'use client';

import React, { useEffect, useState } from 'react';
import { Button, Stack, Typography, CircularProgress, TextField, Box, Container} from '@mui/material';
import styles from './tasks.module.css'; // Import your CSS module for styling


export default function TasksClient() {
  const [tasks, setTasks] = useState([]);
  const [authUrl, setAuthUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [authCode, setAuthCode] = useState(''); // store user input

  const fetchTasks = async (code = null) => {
    setLoading(true);
    try {
      let url = '/api/tasks';
      if (code) url += `?code=${code}`;

      const res = await fetch(url);
      const data = await res.json();

      if (data.authUrl) {
        setAuthUrl(data.authUrl);
      } else if (data.tasks) {
        setTasks(data.tasks);
        setAuthUrl(''); // hide auth section once tasks are loaded
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  if (loading) {
      return (
        <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
          <CircularProgress />
        </Container>
      );
    }

   if (authUrl) {
          {authUrl && (
        <Stack spacing={1}>
          <Typography>1. Open this URL and authorize:</Typography>
          <a href={authUrl} target="_blank" rel="noopener noreferrer">{authUrl}</a>
          <Typography>2. Copy the code from Google and paste it below:</Typography>
          <TextField
            label="Authorization Code"
            value={authCode}
            onChange={(e) => setAuthCode(e.target.value)}
            fullWidth
          />
          <Button
            variant="contained"
            onClick={() => fetchTasks(authCode)}
          >
            Submit Code
          </Button>
        </Stack>
      )}
   }
  return (
   <Box
      sx={{
        display: 'inline-block',
        backgroundImage: 'url(/todo_background.jpg)',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        borderRadius: 5,
        boxShadow: '2.5px 5px 5px rgba(50,50,50,0.6), 3px 6px 7px rgba(50,50,50,0.4), 4px 8px 15px rgba(50,50,50,0.3)',
        width: '100%',
        padding: 2,
        height: 'auto'
      }}
    >
      <Stack spacing={0.5} sx={{ p: 2 }}>
        <Typography variant="h5">TODO List</Typography>
        <hr className={styles.breakline} />
        {tasks.map((task) => (
          <Typography key={task.id} variant="body2">• {task.title} {task.status === 'completed' ? '✅' : ''}</Typography>
        ))}
      </Stack>
    </Box>

  );
}
