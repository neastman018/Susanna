import Image from "next/image";
import styles from "./page.module.css";
import * as React from "react";
import Clock from "./modules/clock/clock";
import CalendarEvents from './modules/calendar/calendar';
import WeatherToday from "./modules/weather/weather";
import { Container, Typography, Box } from "@mui/material";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import '@fontsource/roboto'; // or another font
import PrecipitationIndicator from "./modules/weather/rain.indicator";
import { Google } from "@mui/icons-material";
import TasksClient from "./modules/tasks/tasks";
import Quotes from "./modules/quotes/quotes";
import Alarm from "./modules/alarm/alarm";
import Memories from "./modules/memories/memories";

export default function Home() {
  return (
  <Container className={styles.main} maxWidth={false} spacing={1} disableGutters sx={{padding: 0, margin: 0, width: '100vw', height: '100vh', justifyContent: 'top'}}>
  <Grid container direction="column" justifyContent="top" sx={{ height: '100%', width: '100%', margin: 0 }}>
    {/* Row 1 */}
    <Grid item sx = {{ paddingTop: 2, paddingBottom: 1}}>
      <Grid container direction="row" sx={{ height: '25vh' }}>
        <Grid item xs={3} sx={{width: '25vw'}}>
          <Clock />
        </Grid>
        <Grid item xs={6} sx={{width: '50vw', justifyContent: 'center', display: 'flex'}}>
          <Alarm />
        </Grid>
        <Grid item xs={3} alignContent="right" sx={{width: '25vw', display: 'flex', justifyContent: 'right'}}>
          <WeatherToday city="Blacksburg" apiKey={process.env.NEXT_PUBLIC_OPEN_WEATHER_API_KEY} />
        </Grid>
      </Grid>
    </Grid>

    {/* Row 2 */}
    <Grid item sx={{ paddingTop: 1, paddingBottom: 1}}>
      <Grid container direction="row" sx={{height: '50vh', width: '100%'}}>
        <Grid item xs={3} alignContent="left" sx={{paddingTop: 2, width: '25vw', display: 'flex', justifyContent: 'left', alignSelf: 'flex-start'}}>
          <CalendarEvents icalUrl="https://calendar.google.com/calendar/ical/nick.eastman%40youthapostles.org/public/basic.ics" />
        </Grid>
        <Grid item xs={6} alignContent="center" sx={{width: '50vw', display: 'flex', justifyContent: 'center'}}>

        </Grid>
        <Grid item xs={3} alignContent="right" sx={{paddingTop: 2, width: '25vw', display: 'flex', justifyContent: 'right', alignSelf: 'flex-start'}}>
          <TasksClient />
        </Grid>
      </Grid>
    </Grid>

    {/* Row 3 */}
    <Grid item  sx={{ paddingBottom: 1, alignItems: 'flex-end'}}>
      <Grid container direction="row" sx={{ height: '25vh', width: '100%'}}>
        <Grid item xs={2}></Grid>
        <Grid item xs={8} sx={{display: 'flex', alignItems: 'flex-end'}}><Quotes /></Grid>
        <Grid item xs={2}></Grid>
      </Grid>
    </Grid>
  </Grid>
</Container>

  );
}

