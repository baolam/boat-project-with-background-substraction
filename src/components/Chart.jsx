import React, { Component } from 'react'
import PropTypes from 'prop-types';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts';
import { Box, Typography } from '@mui/material';

function modify_template(head, plotBands, object_name)
{
  let _template = {
    chart : {
      type : "spline"
    },
    title : {
      text : "Example text"
    },
    yAxis : {
      title : {
        text : "Example text 2"
      },
      plotBands : []
    },
    xAxis : {
      type : "datetime",
      title : {
        text : "Time"
      },
      labels : {
        formatter : function()
        {
          let date = new Date();
          return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
        }
      }
    },
    series : []
  };
  _template.title.text = head;
  _template.yAxis.title.text = `${head}`;
  _template.yAxis.plotBands = plotBands;
  _template.series = [ object_name ];
  return _template;
}

class Chart extends Component {
  constructor(props)
  {
    super(props);
    this.__chart = React.createRef();
    this.state = modify_template(this.props.head, this.props.plotBands, this.props.object_data);
  }
  
  componentDidMount()
  {
    this.props.update_reference(this.__chart, this.props.head);
  }

  render() {
    return (
      <Box sx={{
        width : "100%",
        height : 450
      }} >
        <Typography component="h4" variant="h4" style={{
          textAlign : "center"
        }}> Measure {this.props.head}</Typography>
        <HighchartsReact options={this.state} highcharts={Highcharts} ref={this.__chart} />
      </Box>
    )
  }
}

Chart.defaultProps = {
  plotBands : []
}

Chart.propTypes = {
  head : PropTypes.string.isRequired,
  plotBands : PropTypes.array.isRequired,
  object_data : PropTypes.object.isRequired,
  update_reference : PropTypes.func.isRequired
};

export default Chart;