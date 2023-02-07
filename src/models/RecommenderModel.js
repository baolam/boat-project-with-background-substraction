const sequelize = require("sequelize");
const Database = require("../config/database");

const RecommenderModel = Database.define("recommend", {
  feature : {
    type : sequelize.ARRAY(sequelize.FLOAT)
  },
  message : {
    type : sequelize.TEXT
  }
});

const success = require("../config/events/success_db");
success.addListener("success-database", () => {
  RecommenderModel.sync()
  .then(() => {
    console.log("Sync recommender model complete");
  })
  .catch((err) => {
    console.log(err);
    process.exit(0);
  });
});

module.exports = RecommenderModel;