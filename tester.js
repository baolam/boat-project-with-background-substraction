const { config } = require("dotenv");
const path = require("path");

/// Các biến môi trường
config({ path : path.join(__dirname, "src", "config", "enviroment.env") });

const http = require("http");
const socketio = require("socket.io");
const express = require("express");

const app = express();
const server = http.createServer(app);
const io = new socketio.Server(server, { 
  allowEIO3 : true,
  cors : {
    origin : "*"
  }
});

const PORT = process.env.PORT || 4000;
const ip = require("ip");
const url = `http://${ip.address()}:${PORT}`;

const station = io.of("/station");
const boat = io.of("/boat");
const user = io.of("/user");

const cors = require("cors");
const morgan = require("morgan");
const routes = require("./src/routes/routes");

app.use(morgan("dev"));
app.use(cors({ origin : "*" }));
app.use(express.json());
app.use(express.urlencoded({ extended : false }));
app.use(express.static(path.join(__dirname, "src" ,"build")));
app.use("/imgs", require("./src/middleware/imageConnection"));

/// Các đường dẫn
routes(app);
app.get("/test", (req, res) => {
  res.json(req.body);
})

const RecommenderModel = require("./src/models/RecommenderModel");
const RecommenderController = require("./src/controller/RecommenderController");
const standardlize = require("./src/utils/standardlize");
const recommend = new RecommenderController();

/// Kết nối từ người dùng
user.on("connection", (_socket) => {
  _socket.on("control", (command) => {
    console.log(command);
    boat.emit("control", command);
    station.emit("control", command);
  });

});

function time()
{
  let date = new Date();
  return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
}

/// Kết nối từ thuyền
boat.on("connection", (_socket) => {
  /// Một số thông báo từ thiết bị
  _socket.on("notification", (notf) => {
    user.emit("notification", notf);
  });

  /// Thiết bị mất kết nối
  _socket.on("disconnect", () => {
    user.emit("notification", { time : time(), text : "Thuyền bị mất kết nối" });
  });
});

/// Kết nối từ trạm
/***
 * Một bảng record gồm có
 * {
 *   ntu : ...,
 *   tds : ...,
 *   ph : ...,
 *   url : ...,
 *   speed : ...,
 *   code : ...,
 *   x : ...,
 *   y : ...,
 *   time : ...
 * }
 */
station.on("connection", (_socket) => {
  /// Nhận các bản ghi từ thiết bị
  console.log("Có kết nối từ station");

  _socket.on("record", (data) => {
    let _time = data.time;
    data = data.data;
    let feature = [data[0], data[1], data[2]];
    standardlize(feature);
    RecommenderModel.findAll()
    .then((recommends) => {
      let features = recommends.map((recommend) => recommend.toJSON());
      features = features.map((f) => {
        let o = {
          feature : f.feature,
          message : f.message
        };
        return o;
      });
      console.log(data);
      let recommend_result = recommend.run(feature, features.map((f) => f.feature));
      recommend_result.similars.sort((a, b) => a.result < b.result);
      user.emit("recommend", {
        time : _time,
        recommend_result
      });
      user.emit("record", {
        time,
        ntu : data[0],
        tds : data[1],
        ph : data[2],
        x : data[3],
        y : data[4],
        speed : data[5]
      })
    })
  });

  /// Nhận thông báo từ thiết bị
  _socket.on("notification", (notf) => {
    user.emit("notification", notf);
  });
  /// Thiết bị mất kết nối
  _socket.on("disconnect", () => {
    user.emit("notification", { time : time(), 
      text : `Thiết bị trạm mang id ${_socket.id} bị mất kết nối` 
    });
  });
});

let d = 10, prevx = 0, prevy = 0, angle = 0, c = 0;
setInterval(() => {
  let data = {
    ntu : 3500 + Math.floor(Math.random() * 1),
    tds : 500 + Math.floor(Math.random() * 1),
    ph : 7 + Math.round(Math.random() * 1),
    time : (new Date()).getTime(),
    x : prevx + d * Math.cos(angle),
    y : prevy + d * Math.sin(angle),
    speed : Math.floor(Math.random() * 3) + 1
  }
  let _time = data.time;
  let feature = [data.ntu, data.tds, data.ph];
  standardlize(feature);
  RecommenderModel.findAll()
  .then((recommends) => {
    let features = recommends.map((recommend) => recommend.toJSON());
    features = features.map((f) => {
      let o = {
        feature : f.feature,
        message : f.message
      };
      return o;
    });
    let recommend_result = recommend.run(feature, features.map((f) => f.feature));
    recommend_result.similars.sort((a, b) => a.result < b.result);
    user.emit("recommend", {
      time : _time,
      recommend_result,
      features
    });
    user.emit("record", {
      time,
      ntu : data.ntu,
      tds : data.tds,
      ph : data.ph,
      x : data.x,
      y : data.y,
      speed : data.speed
    });
  })
  prevx += d * Math.cos(angle);
  prevy += d * Math.sin(angle);
  c++;
  if (c % 101 == 0)
  {
    angle = -90;
    c = 0;
  } else angle = 0;
}, 5000);

server.listen(PORT, () => {
  console.log(`Kết nối tới đây ${url}`);
});