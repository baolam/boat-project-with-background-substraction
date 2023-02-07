const data = [{"id":1,"feature":[0,0,0.5],"message":"An toàn","createdAt":"2022-12-19T07:11:40.246Z","updatedAt":"2022-12-19T07:11:40.246Z"},{"id":2,"feature":[0,0,0.6428571428571429],"message":"Nước có nhiều hợp chất mang tính bazo","createdAt":"2022-12-19T07:12:24.312Z","updatedAt":"2022-12-19T07:12:24.312Z"},{"id":3,"feature":[0,0,0.5],"message":"An toàn","createdAt":"2022-12-19T07:16:34.890Z","updatedAt":"2022-12-19T07:16:34.890Z"}]

const features = data.map((f) => {
  let o = {
    feature : f.feature,
    message : f.message
  };
  return o;
});

const Recommender = require("./src/controller/RecommenderController");
const recommender = new Recommender();

const result = recommender.run([0, 0, 0], features.map((f) => f.feature));
console.log(result);
console.log(features[result.goal].message);