import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Checkbox,
  CircularProgress,
  Alert,
  Box,
} from '@mui/material';

// --- MOCK DATA: Replace this with your actual API call ---
// This is a sample response structure from the Microsoft Graph API.
const mockTodos = {
  value: [
    { id: '1', title: 'Finalize project proposal', status: 'notStarted' },
    { id: '2', title: 'Schedule team meeting for Q4', status: 'completed' },
    { id: '3', title: 'Review marketing campaign assets', status: 'notStarted' },
    { id: '4', title: 'Submit expense report', status: 'notStarted' },
  ],
};

/**
 * A component to display tasks from a Microsoft To-Do list.
 *
 * @param {object} props - The component props.
 * @param {string} props.accessToken - The Microsoft Graph API access token.
 * @param {string} [props.listId] - The ID of the specific To-Do list. Defaults to the primary task list.
 */
const MicrosoftTodoList = ({ accessToken, listId = 'me/todo/lists/AQMkADAwATMwMAItOTEwNy0zYTMzLTAwAi0wMAoALgAAA9nEXd85hSBAnq4Jg53TwwEA0I1a0a5W_UaJg53TwwEAAAAIBwAAAA==/tasks' }) => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTodos = async () => {
      if (!accessToken) {
        // Using mock data for demonstration if no access token is provided.
        // In a real app, you might want to handle this differently (e.g., show a login prompt).
        console.warn('No access token provided. Using mock data.');
        setTodos(mockTodos.value);
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`https://graph.microsoft.com/v1.0/${listId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch To-Do list. Status: ${response.status}`);
        }

        const data = await response.json();
        setTodos(data.value);
      } catch (err) {
        setError(err.message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, [accessToken, listId]);

  const handleToggle = (id) => {
    setTodos((prevTodos) =>
      prevTodos.map((todo) =>
        todo.id === id
          ? { ...todo, status: todo.status === 'completed' ? 'notStarted' : 'completed' }
          : todo
      )
    );
    // In a real application, you would also make a PATCH request here to update the task's status via the Graph API.
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Error: {error}</Alert>;
  }

  return (
    <Paper elevation={3} sx={{ p: 2, borderRadius: 2, backgroundColor: '#f9f9f9' }}>
      <Typography variant="h5" component="h2" gutterBottom>
        My To-Do List ✅
      </Typography>
      <List>
        {todos.length === 0 ? (
          <ListItem>
            <ListItemText primary="No tasks found. You're all caught up!" />
          </ListItem>
        ) : (
          todos.map((todo) => {
            const isCompleted = todo.status === 'completed';
            return (
              <ListItem
                key={todo.id}
                disablePadding
                sx={{
                  '&:hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.04)',
                  },
                  borderRadius: 1,
                }}
              >
                <ListItemIcon>
                  <Checkbox
                    edge="start"
                    checked={isCompleted}
                    onChange={() => handleToggle(todo.id)}
                    tabIndex={-1}
                    disableRipple
                  />
                </ListItemIcon>
                <ListItemText
                  primary={todo.title}
                  sx={{
                    textDecoration: isCompleted ? 'line-through' : 'none',
                    color: isCompleted ? 'text.secondary' : 'text.primary',
                  }}
                />
              </ListItem>
            );
          })
        )}
      </List>
    </Paper>
  );
};

export default MicrosoftTodoList;