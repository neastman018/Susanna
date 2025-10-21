import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    background: {
      default: '#121212',
      transparent: 'transparent',
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#B0B0B0',
    },
    primary: {
      main: '#50AD5C',
      secondary: '#4b4b4b'
    },
  },
  typography: {
    fontFamily: "'Inter', 'Roboto', 'Helvetica', 'Arial', sans-serif",
    h1: {
      fontSize: '5rem',
    },
    h2: {
      fontSize: '4rem',
    },
    h3: {
      fontSize: '3.0rem',
    },
    h4: {
      fontSize: '2.0rem',
    },
    h5: {
      fontSize: '1.5rem',
    },
    h6: {
      fontSize: '1.25rem',
    },
    body1: {
      fontSize: '1.25rem',
    },
  },

  size : {

  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: 'transparent',
          boxShadow: 'none',
          padding: '0px'
        },
      },
    },
  },
});

export default theme;