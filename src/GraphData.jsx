import React, { Component } from 'react'
import { Grid } from '@mui/material';
import Chart from './components/Chart';

import client from './config/socket';
import { 
  ntu_object, plot_band_ntu, 
  tds_object, plot_band_tds,
  ph_object, plot_band_ph 
} from './config/chart';

import { SOCKET_EVENT } from './config/command';

const LIMIT_RECORD = 7;
class GraphData extends Component {
  constructor(props)
  {
    super(props);

    this.ntu = React.createRef();
    this.tds = React.createRef();
    this.ph = React.createRef();

    /// Dữ liệu của đối tượng
    this.__ntu = [];
    this.__tds = [];
    this.__ph = [];

    this.data = {
      ntu : ntu_object,
      tds : tds_object,
      ph : ph_object
    };

    this.onUpdateReference = this.onUpdateReference.bind(this);
    client.on(SOCKET_EVENT.RECORD, (data) => { this.onRecord(data) });
    /// Thử nghiệm hàm
    // setInterval(() => {
    //   ///console.log("Interepting...");
    //   this.onRecord({
    //     ntu : Math.floor(Math.random() * 4100),
    //     tds : Math.floor(Math.random() * 1300),
    //     ph : Math.floor(Math.random() * 14),
    //     time : (new Date()).getTime()
    //   });
    // }, 5000);
  }

  onUpdateReference(chart, type)
  {
    if (type === "NTU")
      this.ntu = chart;
    else if (type === "PH")
      this.ph = chart;
    else this.tds = chart;
  }

  onRecord(data)
  {
    let { ntu, tds, ph, time } = data;
    this.__ntu.push(
      [ time, ntu ]
    ); 
    this.__tds.push(
      [ time, tds ]
    );
    this.__ph.push(
      [ time, ph ]
    );
    this.__limitRecord(this.__ntu.length);

    this.data.ntu.data = this.__ntu;
    this.data.tds.data = this.__tds;
    this.data.ph.data = this.__ph;
    this.__reference(this.ntu, this.data.ntu);
    this.__reference(this.tds, this.data.tds);
    this.__reference(this.ph, this.data.ph);
  }

  __limitRecord(length)
  {
    while (length > LIMIT_RECORD)
    {
      this.__ntu.shift();
      this.__tds.shift();
      this.__ph.shift();
      length = this.__ntu.length;
    }
  }

  __reference(ref, object_data)
  {
    if (ref !== null && ref.current !== null)
    {
      let chart = ref.current.chart;
      chart.update({ series : [object_data] });
    }
  }

  render() {
    return (
      <Grid container>
        <Grid item xs={4}>
          <Chart head="NTU" 
            object_data={ntu_object} 
            update_reference={this.onUpdateReference}
            plotBands={plot_band_ntu} />
        </Grid>
        <Grid item xs={4}>
          <Chart head="TDS" 
            object_data={tds_object} 
            update_reference={this.onUpdateReference} 
            plotBands={plot_band_tds}
          />
        </Grid>
        <Grid item xs={4}>
          <Chart head="pH" 
            object_data={ph_object} 
            update_reference={this.onUpdateReference} 
            plotBands={plot_band_ph}
          />
        </Grid>
      </Grid>
    )
  }
}

export default GraphData;