// route.js (in /app/api/calendar)
import { RRule } from 'rrule';
import ical from 'ical';

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
    const icsText = await response.text();
    const data = ical.parseICS(icsText);

    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('Error in calendar API:', err);
    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

