import styles from "./page.module.css";
import * as React from "react";
import Clock from "./modules/clock/clock";
import CalendarEvents from './modules/calendar/calendar';
import WeatherToday from "./modules/weather/weather";
import { Container, Box } from "@mui/material";
import Grid from "@mui/material/Grid";
import '@fontsource/roboto'; // or another font
import TasksClient from "./modules/tasks/tasks";
import Quotes from "./modules/quotes/quotes";
import Alarm from "./modules/alarm/alarm";
import Memories from "./modules/memories/memories";
import WordOfDay from "./modules/wordofday/wordofday";

export default function Home() {
  return (
  <Container className={styles.main} maxWidth={false} spacing={1} disableGutters sx={{padding: 0, margin: 0, width: '100vw', height: '100vh', justifyContent: 'top'}}>
  <Grid container direction="row" sx={{ height: '100%', width: '100%', margin: 0 }}>

    {/* Column 1: Clock, Calendar, Memories - compact stack near the top */}
    <Grid size={4} sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'flex-start', pt: 2, px: 2, height: '100%', overflow: 'hidden', minWidth: 0 }}>
      <Clock />
      <CalendarEvents />
      <Memories />
    </Grid>

    {/* Column 2: Alarm anchored top, Quotes anchored bottom spanning ~75% height */}
    <Grid size={4} sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center', height: '100%', pt: 2, overflow: 'hidden', minWidth: 0 }}>
      <Alarm />
      <Box sx={{ height: '75%', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Quotes />
      </Box>
    </Grid>

    {/* Column 3: Weather, Tasks, Word of Day - compact stack near the top */}
    <Grid size={4} sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'flex-end', pt: 2, px: 2, height: '100%', overflow: 'hidden', minWidth: 0 }}>
      <WeatherToday />
      <TasksClient />
      <WordOfDay />
    </Grid>

  </Grid>
  </Container>

  );
}
