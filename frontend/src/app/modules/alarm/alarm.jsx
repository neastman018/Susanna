'use client';
import { Button, Typography } from "@mui/material";
import React, { useEffect, useState } from 'react';
import { useAlarm } from "../../hooks/get_alarm";
import CircularProgress from '@mui/material/CircularProgress';


function getVariant(alarmData) {
    if (!alarmData) return "outlined";
    else return alarmData.armed ? "contained" : "outlined";
}

export default function AlarmButton() {
  const { data: alarmData, isLoading, isError } = useAlarm();
  console.log("Alarm Data:", alarmData);

return (
    <Button
    variant={getVariant(alarmData)}
    sx={{
    borderRadius: 20,
    width: "150px",
    fontWeight: "bold",
    fontSize: "1.5rem",
    color: "#ece3e3ff",
    height: "60px"
    }}
>
    {isLoading ? (
    <CircularProgress size={24} />
    ) : isError ? (
    <Typography>Error</Typography>
    ) : (
    alarmData.alarm_time
    )}
</Button>
);
}