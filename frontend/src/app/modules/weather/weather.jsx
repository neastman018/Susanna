'use client';

import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Box,
} from '@mui/material';
import PrecipitationIndicator from './rain.indicator';
import { useWeather } from '../../hooks/get_weather';
import config from '@app-config/config.json';

const LAT_DEFAULT = config.WEATHER.LATITUDE;
const LON_DEFAULT = config.WEATHER.LONGITUDE;

function toFahrenheit(celsius) {
  return Math.round(((celsius * 9) / 5 + 32) * 10) / 10;
}

function findHigh(weatherData) {
  const today = new Date().toISOString().split('T')[0];
  const todayEntries = weatherData.list.filter((item) =>
    item.dt_txt.startsWith(today)
  );
  if (todayEntries.length === 0) {
    return null;
  }
  return Math.max(...todayEntries.map((item) => item.main.temp_max));
}

function findLow(weatherData) {
  const today = new Date().toISOString().split('T')[0];
  const todayEntries = weatherData.list.filter((item) =>
    item.dt_txt.startsWith(today)
  );
  if (todayEntries.length === 0) {
    return null;
  }
  return Math.min(...todayEntries.map((item) => item.main.temp_min));
}

function isNight(weatherData) {
  const now = new Date();
  const sunrise = new Date(weatherData.city.sunrise * 1000);
  const sunset = new Date(weatherData.city.sunset * 1000);
  return now < sunrise || now > sunset ? 'night' : 'day';
}

function getBackgroundImage(weatherData, condition) {
  const night = isNight(weatherData);
  return `/weatherphotos/${condition}_${night === 'night' ? 'Night' : 'Day'}.jpg`;
}

function getIconImage(weatherData, condition) {
  const night = isNight(weatherData);
  return `/weather_icons/${condition}_${night === 'night' ? 'Night' : 'Day'}.png`;
}

const WeatherToday = ({
  lat = LAT_DEFAULT,
  lon = LON_DEFAULT,
}) => {
  const { data: weatherData, isLoading, isError } = useWeather(lat, lon);

  if (isLoading) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (isError || !weatherData || weatherData.cod !== '200') {
    return (
      <Typography color="error" sx={{ mt: 4 }}>
        Could not fetch weather data.
      </Typography>
    );
  }

  const upcomingForcasts = weatherData.list.slice(0, 5);

  if (upcomingForcasts.length === 0) {
    return (
      <Typography color="textSecondary" sx={{ mt: 4 }}>
        No forecast data for today.
      </Typography>
    );
  }

  const current = upcomingForcasts[0];
  const temperature = current.main.temp;
  const feelsLike = current.main.feels_like;
  const condition = current.weather[0].main;
  const pop = current.pop ?? 0; // precipitation probability (might be undefined)

  return (
    <Box
      sx={{
        display: 'inline-block',
        borderRadius: 5,
        boxShadow: `
          2.5px 5px 5px rgba(50, 50, 50, 0.6),
          3px 6px 7px rgba(50, 50, 50, 0.4),
          4px 8px 15px rgba(50, 50, 50, 0.3)
        `,
        width: '100%',
        height: '12rem',
      }}
    >
      <Card
        sx={{
          color: 'white',
          backgroundImage: `url('${getBackgroundImage(weatherData, condition)}')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          borderRadius: 5,
          height: '12rem',
          width: '100%',
        }}
      >
        <CardContent>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              px: 1,
              pt: 1,
            }}
          >
            {/* Temperature + Feels Like stacked */}
            <Box>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 'bold',
                  lineHeight: 1, // remove vertical gap
                  m: 0,
                }}
              >
                {toFahrenheit(temperature)}°F
              </Typography>
              <Typography
                variant="body1"
                sx={{
                  fontWeight: 'normal',
                  lineHeight: 1, // remove spacing between lines
                  m: 0,
                }}
              >
                Feels Like {toFahrenheit(feelsLike)}°F
              </Typography>
            </Box>

            {/* Precipitation indicator stays right */}
            <PrecipitationIndicator iconSrc={getIconImage(weatherData, condition)} prop={pop} />
          </Box>


          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              paddingTop: 2,
            }}
          >
            <Typography
              variant="h4"
              sx={{
                fontWeight: 'bold',
                px: 1,
                pt: 0,
                borderRadius: 2,
              }}
            >

            {weatherData.city.name}
            </Typography>
            <Typography
              variant="body2"
              sx={{
                fontWeight: 'bold',
                px: 1,
                pt: 0,
                borderRadius: 2,
              }}
            >
              High: {findHigh(weatherData) !== null
                ? toFahrenheit(findHigh(weatherData))
                : '--'}°F <br />
              Low: {findLow(weatherData) !== null
                ? toFahrenheit(findLow(weatherData))
                : '--'}°F
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WeatherToday;
