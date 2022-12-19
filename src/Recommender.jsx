/// https://mui.com/material-ui/react-text-field/
/// https://stackoverflow.com/questions/59647940/how-can-i-use-ref-in-textfield

import React, { Component } from 'react'
import { TextField, Grid, Button, Typography } from '@mui/material';
import my_axios from './config/axiosClient';

class Recommender extends Component {
  constructor(props) {
    super(props);
    this.objects = {
      ntu : React.createRef(),
      tds : React.createRef(),
      ph : React.createRef(),
      message : React.createRef()
    }

    this.onClick = this.onClick.bind(this);
    this.onUpdate = this.onUpdate.bind(this);
    this.onDestroy = this.onDestroy.bind(this);
  }

  passport()
  {
    let feature = Object.keys(this.objects)
      .map((_object) => this.getData(this.objects[_object]));
    let message = feature.pop();
    feature = feature.map((f) => parseFloat(f));
    if (message.length === 0) {
      alert("Không được để trống phần nhập tin nhắn");
      return [false];
    }
    return [true, feature, message];
  }

  onClick()
  {
    let result = this.passport();
    if (! result[0]) return;
    let feature = result[1], message = result[2];
    // console.log(message, feature);
    my_axios.post("/api/recommend", {
      message, feature
    }).then((value) => {
      alert(value.msg);
    }).catch((err) => alert("Lỗi xảy ra khi gửi"));  
  }

  onDestroy()
  {
    let result = this.passport();
    if (! result[0]) return;
    let feature = result[1], message = result[2];
    my_axios.delete("/api/recommend", {
      message, feature
    }).then((value) => {
      alert(value.msg);
    }).catch((err) => alert("Lỗi xảy ra khi gửi"));
  } 

  onUpdate()
  {
    let result = this.passport();
    if (! result[0]) return;
    let feature = result[1], message = result[2];
    my_axios.put("/api/recommend", {
      message, feature
    }).then((value) => {
      alert(value.msg);
    }).catch((err) => alert("Lỗi xảy ra khi gửi"));
  }

  getData(reference)
  {
    return reference.current.value;
  }

  render() {
    return (
      <>
        <Typography variant="h4" 
          component={"h4"} style={{ textAlign : "center" }}
        >
          Recommend
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Typography variant="h6" component={"h6"}>
              NTU
            </Typography>
            <TextField fullWidth 
              type={"number"} inputRef={this.objects.ntu}
              placeholder={"NTU"} 
              defaultValue={0}
            />
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6" component={"h6"}>
              TDS
            </Typography>
            <TextField fullWidth
              type={"number"} inputRef={this.objects.tds}
              placeholder={"TDS"}
              defaultValue={0}
            />
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6" component={"h6"}>
              pH
            </Typography>
            <TextField fullWidth 
              type={"number"} inputRef={this.objects.ph}
              placeholder={"pH"}
              defaultValue={0}
            />
          </Grid>
        </Grid>
        <br />
        <Grid container>
          <TextField fullWidth 
            type={"text"} inputRef={this.objects.message} 
            placeholder={"Recommend"}
            rows={2}
          />
        </Grid>
        <br />
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Button fullWidth variant="outlined"
              onClick={this.onClick} color="success"
            >
              Add new recommend
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button fullWidth variant="outlined"
              onClick={this.onDestroy} color="error"
            >
              Erase recommend
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button fullWidth variant="outlined"
              onClick={this.onUpdate} color="info"
            >
              Update recommend
            </Button>
          </Grid>
        </Grid>
      </>
    )
  }
}

export default Recommender;