const path = require("path");

/**
 * 
 * @param {*} app
 * @method 
 */
function route(app)
{
  app.use("/api/recommend", require("./recommend"));
  app.use("/api/background", require("./background"));
  app.get("/", (req, res) => {
    res.sendFile(
      path.join(__dirname, "../", "build", "index.html")
    );
  })
}

module.exports = route;