import React, { Component } from 'react'
import { Typography, Box, Grid } from '@mui/material';

import Trace from './components/Trace';
import DetailInformation from './components/DetailInformation';

class BoatInformation extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      speed : "None",
      direction : "None"
    }
  }

  render() {
    return (
      <Box style={{ height : 450, width : "100%" }}>
        <Typography component="h4" variant="h4" style={{ textAlign : "center" }}>Boat parameters</Typography>
        <Grid container>
          <Grid item xs={2} >
            <DetailInformation />            
          </Grid>
          <Grid>
            <Trace height={450} width={250} />
          </Grid>
        </Grid>
      </Box>
    )
  }
}

export default BoatInformation;