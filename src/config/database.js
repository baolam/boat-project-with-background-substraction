const sequelize = require("sequelize");

const Database = new sequelize.Sequelize({
  database : process.env.DATABASE_NAME,
  username : process.env.DATABASE_USER,
  password : process.env.DATABASE_PASSWORD,
  port : process.env.DATABASE_PORT,
  dialect : "postgres",
  logging : false
});

Database.sync()
.then(() => {
  let success = require("./events/success_db");
  success.emit("success-database");
  console.log("Kết nối đến database thành công");
})
.catch((err) => {
  console.log(err);
  process.exit(0);
});

module.exports = Database;