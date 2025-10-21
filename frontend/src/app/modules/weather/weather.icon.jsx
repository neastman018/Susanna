import React from 'react';
'use client'; // For Next.js App Router

const conditionToIcon = {
    Clear_Day: '01d',
    Clear_Night: '01n',
    Few_Clouds_Day: '02d',
    Few_Clouds_Night: '02n',
    Scattered_Clouds_Day: '03d',
    Scattered_Clouds_Night: '03n',
    Broken_Clouds_Day: '04d',
    Broken_Clouds_Night: '04n',
    Rain_Day: '09d',
    Rain_Night: '09n',
    Drizzle_Day: '10d',
    Drizzle_Night: '10n',
    Thunderstorm_Day: '11d',
    Thunderstorm_Night: '11n',
    Snow_Day: '13d',
    Snow_Night: '13n',
    Mist_Day: '50d',
    Mist_Night: '50n',
    // Add more mappings as needed
};

const WeatherIcon = ({ condition }) => {
    const icon = conditionToIcon[condition] || '01d'; // default to 'Clear'
    return (
        <img
            src={`/weather_icon/${icon}@2x.png`}
            alt={condition}
            style={{ width: 48, height: 48 }}
        />
    );
};

export default WeatherIcon;
