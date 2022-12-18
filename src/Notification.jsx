import React, { Component } from 'react'
import client from './config/socket';

import { Box, 
  List, ListItem, 
  ListItemText,
  ListItemAvatar, 
  Avatar,
  Typography
} from '@mui/material';
import { Notifications, Done, SmsFailed } from '@mui/icons-material';
import { SOCKET_EVENT } from './config/command';

class ItemData extends Component {
  constructor(props)
  {
    super(props);
  }

  render()
  {
    let { avatar, time, msg } = this.props;
    return (
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar>
            { avatar === undefined ? <Notifications /> : avatar }
          </Avatar>
        </ListItemAvatar>
        <ListItemText primary={time} secondary={
          <React.Fragment>
            <Typography
              sx={{ display: 'inline' }}
              component="span"
              variant="body2"
              color="text.primary"
            >
              Thông báo
            </Typography>
            {" - "}{msg}
          </React.Fragment>
        } />
      </ListItem>
    )
  }
}

class Notification extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      notifications : []
    };

    client.on(SOCKET_EVENT.BOAT, (upd) => this.addEventBoat(upd) );
    client.on(SOCKET_EVENT.DEVICE, (upd) => this.addEventDevice(upd) );
  }

  formatOnTime()
  {
    let date = new Date();
    return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
  }

  __notification_object(update_state, msgs, avatars)
  {
    let obj = {
      time : this.formatOnTime(),
      msg : msgs[0],
      avatar : avatars[0]
    }
    /// Không đáp ứng điều kiện
    if (! update_state)
    {
      obj.msg = msgs[1];
      obs.avatar = avatars[1]
    }
    return obj;
  }

  addEventBoat(update_state)
  {    
    let obj = this.__notification_object(update_state, [
      "Đã có kết nối giữa người dùng và thiết bị",
      "Chưa có kết nối giữa người dùng và thiết bị"
    ], [
      <Done />, <SmsFailed />
    ]);
    let notf = this.state.notifications;
    notf.push(obj);
    this.setState({ notification : notf });
  }

  addEventDevice(update_state)
  {
    let obj = this.__notification_object(update_state, [
      "Đã có kết nối với Arduino",
      "Chưa có kết nối với arduino"
    ], [
      <Done />, <SmsFailed />
    ]);
    let notf = this.state.notifications;
    notf.push(obj);
    this.setState({ notification : notf });
  }

  render() {
    return (
      <Box>
        <List>
          {this.state.notifications.map((notification) => {
            return (
              <ItemData key={notification.time} time={notification.time} 
                msg={notification.msg} avatar={notification.avatar} />
            );
          })}
        </List>
      </Box>
    )
  }
}

export default Notification;