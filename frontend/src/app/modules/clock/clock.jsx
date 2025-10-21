"use client";
import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import styles from "./clock.module.css"; // Import the CSS module for styling




export default function Clock() {
  const [isMounted, setIsMounted] = useState(false);
  const [currentTime, setCurrentTime] = useState({
    time: "",
    date: {
      weekday: "",
      month: "",
      day: "",
      year: "",
    },
  });

  useEffect(() => {
    setIsMounted(true);

    if (isMounted) {
      const updateTime = () => {
        const now = new Date();
        setCurrentTime({
          time: now.toLocaleTimeString("en-GB", { hour12: false }),
          date: {
            weekday: now.toLocaleDateString("en-GB", { weekday: "long" }),
            month: now.toLocaleDateString("en-GB", { month: "long" }),
            day: now.getDate(),
            year: now.getFullYear(),
          },
        });
      };

      updateTime(); // Initialize with the current time immediately
      const interval = setInterval(updateTime, 1000); // Update time every second
      return () => clearInterval(interval); // Cleanup interval
    }
  }, [isMounted]);

  if (!isMounted) {
    return null; // Avoid rendering on the server
  }

return (
  <Box>
    <Typography variant="h2" color = "text.primary" 
      sx = {{marginTop: '16px', marginLeft: '16px'}}>
      {currentTime.time}
    </Typography>

    <hr className={styles.breakline}/>

    <Typography variant="h4" color = "text.secondary"
      sx = {{marginLeft: '16px'}}>
      {currentTime.date.weekday}
    </Typography>
    <Typography variant="h4" color = "text.secondary"
      sx = {{marginLeft: '16px'}}>
      {currentTime.date.month} {currentTime.date.day}, {currentTime.date.year}
    </Typography>
  </Box>
);
}
