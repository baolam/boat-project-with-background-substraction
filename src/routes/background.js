const express = require("express");
const Router = express.Router();

const multer = require("multer");
const path = require("path");
const storage = new multer.diskStorage({
  filename : function (req, file, cb)
  {
    cb(null, "background")
  },
  destination : path.join(__dirname, "../", "imgs")
});

const upload = multer({ storage });

module.exports = Router;