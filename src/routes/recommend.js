const express = require("express");
const Router = express.Router();

const Recommender = require("../controller/RecommenderController");
const RecommenderModel = require("../models/RecommenderModel");
const controller = new Recommender();
const standardlize = require("../utils/standardlize");

Router.get("/", (req, res) => {
  /// Đặc trưng gồm có nồng độ ntu, nồng độ tds, độ ph
  let feature = standardlize(req.body.feature);
  RecommenderModel.findAll()
  .then((fs) => {
    let f_json = fs.map((f) => f.toJSON());
    let r = controller.run(feature, f_json);
    res.json(r);
  });
});

Router.put("/", (req, res) => {
  let feature = standardlize(req.body.feature);
  let message = req.body.message;
  RecommenderModel.update({
    feature, message
  }, {
    where : {
      message
    }
  })
  .then(() => {
    res.json({ msg : "Cập nhật thành công" });
  })
  .catch(() => {
    res.json({ msg : "Cập nhật thất bại" });
  });
})

Router.get("/record", (req, res) => {
  RecommenderModel.findAll()
  .then((fs) => {
    let f_json = fs.map((f) => f.toJSON());
    res.json(f_json);
  })
});

Router.get("/threshold", (req, res) => {
  let result = req.params.theta;
  controller.theta = parseFloat(result);
});

Router.post("/", (req, res) => {
  let feature = standardlize(req.body.feature);
  let message = req.body.message;
  RecommenderModel.findOne({
    where : {
      message
    }
  }).then((v) => {
    v.toJSON();
    res.json({ msg : "Tin nhắn đã tồn tại" });
  })
  .catch(() => {
    RecommenderModel.create({
      feature,
      message
    })
    .then(() => {
      res.json({ msg : "Tạo đề xuất thành công" });
    })
    .catch((err) => {
      console.log(err);
      res.json({ msg : "Tạo đề xuất thất bại" });
    });
  });
});

Router.delete("/", (req, res) => {
  let message = req.body.message;
  RecommenderModel.destroy({
    where : {
      message
    }
  })
  .then(() => {
    res.json({ msg : "OK" });
  })
  .catch(() => {
    res.json({ msg : "Failed" });
  });
});

module.exports = Router;