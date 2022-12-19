import axios from "axios";

const my_axios = axios.create({
  baseURL : "http://localhost:4000"
});

my_axios.interceptors.response.use((object) => {
  return object.data;
})

export default my_axios;