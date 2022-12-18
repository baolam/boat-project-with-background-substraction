import React, { Component } from 'react'
import { Grid } from '@mui/material';
import Chart from './components/Chart';

import client from './config/socket';
import { ntu_object, tds_object } from './config/chart';

import { SOCKET_EVENT } from './config/command';
import { LEVEL_1 as tds_1, LEVEL_2 as tds_2, LEVEL_3 as tds_3, LEVEL_4 as tds_4 } from './config/tds';
import { LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8 } from './config/ntu';

const LIMIT_RECORD = 20;
class GraphData extends Component {
  constructor(props)
  {
    super(props);

    this.ntu = React.createRef();
    this.tds = React.createRef();

    /// Dữ liệu của đối tượng
    this.__ntu = [];
    this.__tds = [];
    this.data = {
      ntu : ntu_object,
      tds : tds_object
    };

    this.onUpdateReference = this.onUpdateReference.bind(this);
    client.on(SOCKET_EVENT.RECORD, (data) => { this.onRecord(data) });
    /// Thử nghiệm hàm
    // setInterval(() => {
    //   ///console.log("Interepting...");
    //   this.onRecord({
    //     ntu : Math.floor(Math.random() * 4100),
    //     tds : Math.floor(Math.random() * 1300)
    //   });
    // }, 5000);
  }

  onUpdateReference(chart, type)
  {
    if (type === "NTU")
      this.ntu = chart;
    else this.tds = chart;
  }

  onRecord(data)
  {
    let { ntu, tds } = data;
    this.__ntu.push(ntu); this.__tds.push(tds);
    this.data.ntu.data = this.__ntu;
    this.data.tds.data = this.__tds;
    this.__limitRecord(this.data.ntu.length);
    this.__reference(this.ntu, this.data.ntu);
    this.__reference(this.tds, this.data.tds);
  }

  __limitRecord(length)
  {
    console.log(length);
    if (length > LIMIT_RECORD)
    {
      this.data.ntu.data.shift();
      this.data.tds.data.shift();
    }
  }

  __reference(ref, object_data)
  {
    ///console.log(ref.current !== null);
    if (ref !== null && ref.current !== null)
    {
      let chart = ref.current.chart;
      chart.update({ series : [object_data] });
    }
  }

  render() {
    return (
      <Grid container>
        <Grid item xs={6}>
          <Chart head="NTU" 
            object_data={ntu_object} 
            update_reference={this.onUpdateReference}
            plotBands={[
              {
                from : 4000,
                to: 10000,
                color : LEVEL_1,
                label : {
                  text : "Unacceptable",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 3000,
                to : 4000,
                color : LEVEL_2,
                label : {
                  text : "least",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 2000,
                to : 3000,
                color : LEVEL_3,
                label : {
                  text : "okay",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 1000,
                to : 2000,
                color : LEVEL_4,
                label : {
                  text : "Pretty good",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 250,
                to : 1000,
                color : LEVEL_5,
                label : {
                  text : "Stable",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 0,
                to : 250,
                color : LEVEL_7,
                label : {
                  text : "Good",
                  style : {
                    color : "white"
                  }
                }
              }
            ]} />
        </Grid>
        <Grid item xs={6}>
          <Chart head="TDS" 
            object_data={tds_object} 
            update_reference={this.onUpdateReference} 
            plotBands={[
              {
                from : 300,
                t0 : 600,
                color : tds_1,
                label : {
                  text : "Good",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 600,
                to : 900,
                color : tds_2,
                label : {
                  text : "Fair",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 900,
                to : 1200,
                color : tds_3,
                label : {
                  text : "Poor",
                  style : {
                    color : "white"
                  }
                }
              },
              {
                from : 1200,
                to : 12000,
                color : tds_4,
                label : {
                  text : "Unacceptable",
                  style : {
                    color : "white"
                  }
                }
              }
            ]}
          />
        </Grid>
      </Grid>
    )
  }
}

export default GraphData;