import { RRule } from 'rrule';
import ical from 'ical';

// Define how far into the future we want to expand recurring events (e.g., 30 days)
const RECURRENCE_END_DAYS = 30;

/**
 * Expands a single event object with an RRULE into an array of specific instances.
 * @param {Object} event - The event object parsed by ical.js.
 * @returns {Array<Object>} An array of event instances.
 */
function expandRecurrence(event) {
    // If there's no RRULE, it's a simple, non-recurring event.
    if (!event.rrule) {
        return [{ ...event, isRecurring: false }];
    }

    try {
        // Define the expansion period
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const endDate = new Date(today);
        endDate.setDate(today.getDate() + RECURRENCE_END_DAYS);

        // 1. Get the recurrence rule string
        const ruleString = event.rrule.toString();

        // 2. Determine the start date (DTSTART)
        // Use the event's start date, or default to now if missing/invalid
        let startDate = event.start instanceof Date ? event.start : today;

        // 3. Create the RRule object
        const rule = RRule.fromString(ruleString);
        
        // Ensure the rule starts from the event's DTSTART time
        const expandedRule = new RRule({
            ...rule.options,
            dtstart: startDate,
        });

        // 4. Generate all occurrences within the specified time window
        const dates = expandedRule.between(today, endDate, true);

        // 5. Calculate duration once
        const durationMs = event.end.getTime() - event.start.getTime();

        // 6. Map the dates back to event objects, handling All-Day events and DST shifts
        if (event.datetype === 'date') {
            // ALL DAY EVENT FIX: Force start/end to be midnight UTC to prevent time shifts.
            const instances = dates.map(date => {
                // Set the start date to midnight UTC on the calculated day
                const allDayStart = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
                
                return {
                    ...event,
                    start: allDayStart,
                    // Reapply the original duration (typically 24 hours)
                    end: new Date(allDayStart.getTime() + durationMs), 
                    isRecurring: true,
                    originalUid: event.uid
                };
            });
            return instances;
        } else {
            // TIME-ZONED EVENT DST FIX: Selectively edit the time components.
            // Get the original wall-clock time from the initial event start date (local time of the server/environment)
            const originalHour = event.start.getHours();
            const originalMinute = event.start.getMinutes();
            const originalSecond = event.start.getSeconds();

            const instances = dates.map(date => {
                // 1. Create a new Date object based on the expanded date (YYYY-MM-DD)
                const newStart = new Date(date);
                
                // 2. Set the time components to the original wall-clock time (e.g., 10:00 AM).
                // This forces the new date to observe the correct local time, correcting the DST shift.
                newStart.setHours(originalHour, originalMinute, originalSecond, 0);

                return {
                    ...event,
                    start: newStart, 
                    // Calculate end time based on the corrected start time + fixed duration
                    end: new Date(newStart.getTime() + durationMs), 
                    isRecurring: true,
                    originalUid: event.uid
                };
            });
            return instances;
        }

    } catch (e) {
        console.error("Error expanding RRULE for event:", event.uid, e);
        // If expansion fails, just return the original event as a fallback
        return [{ ...event, isRecurring: false, expansionError: true }];
    }
}

export async function GET(req) {
  try {
    const url = new URL(req.url);
    const calendarUrl = url.searchParams.get('url');

    if (!calendarUrl) {
      return new Response(JSON.stringify({ error: 'Missing url parameter' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Optional: validate it's a proper URL
    try {
      new URL(calendarUrl);
    } catch {
      return new Response(JSON.stringify({ error: 'Invalid URL' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const response = await fetch(calendarUrl);
    
    if (!response.ok) {
        throw new Error(`Failed to fetch ICS file: ${response.statusText}`);
    }

    const icsText = await response.text();
    const data = ical.parseICS(icsText);

    // Filter out VTIMEZONE components and get only VEVENTs
    const calendarComponents = Object.values(data).filter(component => component.type === 'VEVENT');

    // Array to hold all final event instances (including expanded recurrences)
    let finalEvents = [];

    calendarComponents.forEach(event => {
        if (event.rrule) {
            // Expand recurring events
            finalEvents.push(...expandRecurrence(event));
        } else {
            // Add non-recurring events directly
            finalEvents.push(event);
        }
    });

    return new Response(JSON.stringify(finalEvents), {
      headers: { 'Content-Type': 'application/json' },
    });

  } catch (err) {
    console.error('Error in calendar API:', err);
    return new Response(JSON.stringify({ error: 'Internal Server Error', details: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}