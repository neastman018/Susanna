'use client';

import React, { useEffect, useState } from 'react';
import { Card, Box } from '@mui/material';
import { frostedCardSx } from '../../components/FrostedCard';

const imageHeight = 15; // in rem

function useRotatingBackgroundImage(intervalMs = 5 * 60 * 1000) {
  const [images, setImages] = useState([]);
  const [backgroundImage, setBackgroundImage] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch('/api/memories')
      .then((res) => res.json())
      .then((data) => {
        if (!cancelled && Array.isArray(data.images)) {
          setImages(data.images);
        }
      })
      .catch((err) => console.error('Failed to fetch memories:', err));
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (images.length === 0) return;

    const pickRandom = () => {
      const randomIndex = Math.floor(Math.random() * images.length);
      setBackgroundImage(images[randomIndex]);
    };

    pickRandom();
    const interval = setInterval(pickRandom, intervalMs);

    return () => clearInterval(interval);
  }, [images, intervalMs]);

  return backgroundImage;
}

export default function Memories() {
  const bgImage = useRotatingBackgroundImage();

  return (
    <Box
      sx={{
        display: 'inline-block',
        ...frostedCardSx,
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
