export const ntu_object = {
  name : "NTU",
  color : "white",
  data : []
};

export const tds_object = {
  name : "TDS",
  color : "yellow",
  data : []
};

export const template = {
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
      text : "Thời gian"
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

function object_plot_band(from, to, color, text, color_text)
{
  let obj = {
    from, to, color,
    label : {
      text,
      style : {
        color : color_text
      }
    }
  }
  return obj;
}

export const plot_band = object_plot_band;