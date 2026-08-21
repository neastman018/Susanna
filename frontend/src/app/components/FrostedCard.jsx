import Box from '@mui/material/Box';

export const frostedCardSx = {
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  borderRadius: 5,
  boxShadow: `
    2.5px 5px 5px rgba(50, 50, 50, 0.6),
    3px 6px 7px rgba(50, 50, 50, 0.4),
    4px 8px 15px rgba(50, 50, 50, 0.3)
  `,
};

export default function FrostedCard({ children, sx = {}, ...rest }) {
  return (
    <Box sx={{ ...frostedCardSx, ...sx }} {...rest}>
      {children}
    </Box>
  );
}
