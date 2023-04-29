import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import { Grid, Typography, TextField, Button, List, ListItem, ListItemText } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(2),
  },
  inputField: {
    margin: theme.spacing(1),
  },
  button: {
    margin: theme.spacing(1),
  },
  list: {
    marginTop: theme.spacing(2),
  },
}));

function App() {
  const classes = useStyles();
  const [eventData, setEventData] = useState('');
  const [output, setOutput] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchOutput();
  }, []);

  const handleInputChange = (event) => {
    setEventData(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    const response = await axios.post('/handle_event', { data: eventData });
    setLoading(false);
    setEventData('');
    fetchOutput();
  };

  const fetchOutput = async () => {
    const response = await axios.get('/output');
    setOutput(response.data);
  };

  return (
    <div className={classes.root}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={6}>
          <Typography variant="h4">Event Input</Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              id="event-data"
              label="Event Data"
              variant="outlined"
              fullWidth
              multiline
              rows={4}
              value={eventData}
              onChange={handleInputChange}
              className={classes.inputField}
            />
            <Button
              variant="contained"
              color="primary"
              type="submit"
              disabled={!eventData || loading}
              className={classes.button}
            >
              Submit
            </Button>
          </form>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="h4">Event Output</Typography>
          <List className={classes.list}>
            {output.map((item, index) => (
              <ListItem key={index}>
                <ListItemText primary={item} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
