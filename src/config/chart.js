export const ntu_object = {
  name : "NTU",
  color : "white",
  data : []
};

export const tds_object = {
  name : "TDS",
  color : "white",
  data : []
};

export const ph_object = {
  name : "pH",
  color : "green",
  data : []
}

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

const tds_level = {
  LEVEL_1 : "#309FE6",
  LEVEL_2 : "#28AEB1",
  LEVEL_3 : "#1B4578",
  LEVEL_4 : "#B81A17"
}

const ntu_level = {
  LEVEL_1 : "#99270D",
  LEVEL_2 : "#AF3912",
  LEVEL_3 : "#C7460F",
  LEVEL_4 : "#D97515",
  LEVEL_5 : "#E0B150",
  LEVEL_6 : "#E0CA99",
  LEVEL_7 : "#DEDBD4",
  LEVEL_8 : "#D5DCE3"
};

export const plot_band_ntu = [
  {
    from : 4000,
    to: 10000,
    color : ntu_level.LEVEL_1,
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
    color : ntu_level.LEVEL_2,
    label : {
      text : "Least",
      style : {
        color : "white"
      }
    }
  },
  {
    from : 2000,
    to : 3000,
    color : ntu_level.LEVEL_3,
    label : {
      text : "Okay",
      style : {
        color : "white"
      }
    }
  },
  {
    from : 1000,
    to : 2000,
    color : ntu_level.LEVEL_4,
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
    color : ntu_level.LEVEL_5,
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
    color : ntu_level.LEVEL_6,
    label : {
      text : "Good",
      style : {
        color : "white"
      }
    }
  }
]

export const plot_band_tds = [
  {
    from : 0,
    to : 600,
    color : tds_level.LEVEL_1,
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
    color : tds_level.LEVEL_2,
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
    color : tds_level.LEVEL_3,
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
    color : tds_level.LEVEL_4,
    label : {
      text : "Unacceptable",
      style : {
        color : "white"
      }
    }
  }
]

export const plot_band_ph = [
  {
    from : 0,
    to : 6,
    color : "red",
    label : {
      text : "Axit",
      style : {
        color : "white"
      }
    }
  },
  {
    from : 7,
    to : 7,
    color : "green",
    label : {
      text : "Ok",
      style : {
        color : "black"
      }
    }
  },
  {
    from : 8,
    to : 14,
    color : "yellow",
    label : {
      text : "Bazo",
      style : {
        color : "red"
      }
    }
  }
];