'use client'; // for Next.js App Router
import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Container,
  CircularProgress,
  Stack,
  Box
} from '@mui/material';
import styles from './calendar.module.css'; // Import your CSS module for styling
import config from '../../../../../config.json';

const icalUrl = config.CALENDARS.PRIMARY.ICAL_URL;


const CalendarEvents = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCalendar = async () => {
      try {
        const res = await fetch(`/api/calendar?url=${encodeURIComponent(icalUrl)}`);
        const data = await res.json();
        setEvents(data);
        console.log('Fetched events:', data);
      } catch (error) {
        console.error('Error fetching calendar:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCalendar();
  }, [icalUrl]);

  if (loading) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }


  // Filter events for today only
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);

  const todaysEvents = events
    .filter((event) => {
      const start = new Date(event.start);
      return start >= today && start < tomorrow;
    })
    .sort((a, b) => new Date(a.start) - new Date(b.start));



  return (
    <Box
      sx={{
        display: 'inline-block',
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        borderRadius: 5,
        boxShadow: `
          2.5px 5px 5px rgba(50, 50, 50, 0.6),
          3px 6px 7px rgba(50, 50, 50, 0.4),
          4px 8px 15px rgba(50, 50, 50, 0.3)
        `,
        width: '100%',
        padding: 2,
      }}
    >
      <Typography variant="h5" align="left">
        Today's Events
      </Typography>

      <hr className={styles.breakline} />

      <Stack spacing={0}>
        {todaysEvents.map((event, idx) => {
          const now = new Date();
          const start = new Date(event.start);
          const end = new Date(event.end);

          // Determine background color
          let bgColor = 'transparent'; // default
          if (now >= start && now <= end) {
            bgColor = 'rgba(255, 0, 0, 0.2)'; // event is happening → red
          } else if (now < start) {
            // next upcoming event gets yellow
            const nextEvent = todaysEvents.find(
              (e) => new Date(e.start) > now
            );
            if (nextEvent && nextEvent.start === event.start) {
              bgColor = 'rgba(255, 255, 0, 0.2)'; // next event → yellow
            }
          } else if (now > start) {
            bgColor = 'rgba(0, 255, 0, 0.2)'; // event has ended → green
          }

          return (
            <Card
              key={idx}
              sx={{
                m: 0,
                p: 0,
                boxShadow: 'none',
                borderRadius: 0,
                borderBottom: idx < todaysEvents.length - 1 ? '1px solid #333' : 'none',
              }}
            >
              <CardContent sx={{ p: '2px 6px !important' }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    backgroundColor: bgColor,
                    padding: 0.5,
                    borderRadius: 2,
                  }}
                >
                  <Typography
                    variant="body2"
                    align="left"
                    sx={{
                      m: 0,
                      maxWidth: '60%',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                    title={event.summary}
                  >
                    {event.summary}
                  </Typography>
                  <Typography
                    variant="body2"
                    align="right"
                    sx={{ m: 0, whiteSpace: 'nowrap', color: 'gray' }}
                  >
                    {start.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: false })}
                    {' - '}
                    {end.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: false })}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          );
        })}
      </Stack>
    </Box>
  );
};

export default CalendarEvents;
