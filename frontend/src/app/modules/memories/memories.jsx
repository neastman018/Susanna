'use client';

import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';

const imageHeight = 15; // in rem

function useRandomBackgroundImage(intervalMs = 5 * 60 * 1000) {
  const images = [
    '/memories/photo1.jpg',
    '/memories/photo2.jpg',
    '/memories/photo3.jpg',
    '/memories/photo4.jpg',
    '/memories/photo5.jpg',
    '/memories/photo6.jpg',
    '/memories/photo7.jpg',
    '/memories/photo8.jpg',
  ];



  const [backgroundImage, setBackgroundImage] = useState(null);

  useEffect(() => {
    // pick first random image when client mounts
    const randomIndex = Math.floor(Math.random() * images.length);
    setBackgroundImage(images[randomIndex]);

    // change periodically
    const interval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * images.length);
      setBackgroundImage(images[randomIndex]);
    }, intervalMs);

    return () => clearInterval(interval);
  }, [intervalMs]);

  return backgroundImage;
}

export default function Memories() {
  const bgImage = useRandomBackgroundImage();

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
        width: `${imageHeight * 1.5}rem`,
        height: `${imageHeight * 1}rem`,
      }}
    >
      <Card
        sx={{
          color: 'white',
          backgroundImage: bgImage ? `url('${bgImage}')` : 'none', // <- safe
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          height: '100%',
          width: '100%',
          borderRadius: 5,
          display: 'flex',
          flexDirection: 'column',
          padding: 0,
        }}
      >
      </Card>
    </Box>
  );
}
