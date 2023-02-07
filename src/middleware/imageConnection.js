const path = require("path");

function connection(req, res, next)
{
  let file_name = req.path;
  if (file_name == '/')
  {
    res.send("Lấy file ảnh");
  }
  else {
    res.sendFile(
      path.join(__dirname, "../", "imgs", file_name)
    );
  }
}

module.exports = connection;