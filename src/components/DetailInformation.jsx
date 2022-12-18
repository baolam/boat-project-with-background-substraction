import React, { Component } from 'react'
import { 
  Typography, 
  List, 
  ListItem,
  ListItemText 
} from '@mui/material';
import { LEFT, RIGHT } from '../config/command';
import client from '../config/socket';

class DetailInformation extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      speed : "None",
      direction : "None",
      notification : []
    }

    client.on("POSITION", (data) => {
      let { speed, code } = data;
      let command = "FORWARD";
      if (code === LEFT)
        command = "LEFT";
      else if (code === RIGHT)
        command = "RIGHT";
      else command = "STOP";
      this.setState({
        speed,
        direction : command
      });
    });

    client.on("notification", (data) => {
      let notfs = [...this.state.notification];
      notfs.push(data);
      if (notfs.length > 4)
        notfs.shift();
      this.setState({
        notification : notfs
      });
    });
  }

  render() {
    return (
      <>
        <Typography component="h5" variant="h5">  Speed: {this.state.speed}</Typography>
        <Typography> Code: {this.state.direction}</Typography>
        <List>
          {this.state.notification.map((r) => 
            <ListItem>
              <ListItemText>At: { r.time }, { r.text }</ListItemText>
            </ListItem>
          )}
        </List>
      </>
    )
  }
}

export default DetailInformation; 