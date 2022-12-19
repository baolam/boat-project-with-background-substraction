import React, { Component } from 'react'
import { Box, Button, Grid, Typography } from '@mui/material';
import client from './config/socket';
import { FORWARD, STOP, LEFT, RIGHT, TRACK_GARBAGE } from './config/command';

class ControlBoat extends Component {
  constructor(props)
  {
    super(props);
    this.controlBoat = this.controlBoat.bind(this);
  }

  controlBoat(command)
  {
    client.emit("control", command);
  }

  render() {
    return (
      <Box>
        <Typography 
          variant="h4" 
          component="h4" 
          style={{ textAlign : "center" }}>
            Control (By hand)
        </Typography>
        <Grid container spacing={1}>
          <Grid item xs={2}>
            <Button 
              fullWidth 
              variant="outlined"
              color="primary" 
              onClick={() => this.controlBoat(LEFT)} >
                Left
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button 
              fullWidth 
              variant="outlined"
              color="warning"
              onClick={() => this.controlBoat(FORWARD)}> 
                Forward
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button 
              fullWidth 
              variant="outlined"
              color="warning"
              onClick={() => this.controlBoat(STOP)}>
                Stop
            </Button>
          </Grid>
          <Grid item xs={2}>
            <Button 
              fullWidth 
              variant="outlined"
              color="primary"
              onClick={() => this.controlBoat(RIGHT)}>
                Right
            </Button>
          </Grid>
        </Grid>
        <br />
        <Grid container spacing={1}>
          <Grid item xs={4}>
            <Button
              fullWidth
              variant="outlined"
              color="success"
              onClick={() => client.emit(TRACK_GARBAGE)}
            >
              Track garbage
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button
              fullWidth
              variant="outlined"
              color="success"
              onClick={() => client.emit("UPDATE_BACKGROUND")}
            >
              Update enviroment image
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button
              fullWidth
              variant="outlined"
              color="success"
              onClick={() => {
                let speed = prompt("New speed");
                speed = parseInt(speed);
                client.emit("UPDATE_SPEED", speed);
              }}
            >
              Update speed of boat
            </Button>
          </Grid>
        </Grid>
      </Box>
    )
  }
}

export default ControlBoat;