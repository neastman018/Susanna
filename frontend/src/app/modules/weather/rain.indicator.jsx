import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

const iconSize = 3; // in rem
const progressSize = iconSize * 1.25;
const circleSize = iconSize * 1.375;

const boxWidth = 6; // in rem

const circlePadding = (boxWidth - circleSize) / 2;
const progressPadding = (boxWidth - progressSize) / 2;
const iconPadding = (boxWidth - iconSize) / 2;





const PrecipitationIndicator = ({ icon, prop }) => {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex', width: '6rem', height: '6rem' }}>
      
      {/* Background circle */}
      <Box
        sx={{
          position: 'absolute',
          top: `${circlePadding}rem`,
          left: `${circlePadding}rem`,
          width: `${circleSize}rem`,
          height: `${circleSize}rem`,
          borderRadius: '50%',
          backgroundColor: 'rgba(200, 200, 200, 0.7)',
          zIndex: 0,
        }}
      />

      {/* Circular progress */}
      <CircularProgress
        variant="determinate"
        value={prop * 100}
        size={`${progressSize}rem`}
        thickness={4}
        sx={{
          position: 'absolute',
          top: `${progressPadding}rem`,
          left: `${progressPadding}rem`,
          transform: 'translate(-50%, -50%)',
          zIndex: 1,
          color: 'rgba(40,119,27,1)',
        }}
      />

      {/* Weather icon */}
      <Box
        sx={{
          position: 'absolute',
          top: `${iconPadding}rem`,
          left: `${iconPadding}rem`,
          zIndex: 2,
          backgroundColor: 'transparent',
        }}
      >
        <img
          src={`https://openweathermap.org/img/wn/${icon}@2x.png`}
          alt='weather icon'
          style={{ width: `${iconSize}rem`, height: `${iconSize}rem` }}
        />
      </Box>
    </Box>
  );
};

export default PrecipitationIndicator;
