import axios from 'axios';

const service = axios.create({
  baseURL:'http://81.68.174.36:8080',
  timeout: 5000,
});
let token = window.localStorage.getItem("token")
service.interceptors.request.use(function(config){ 
  config.headers["Authorization"] = "Bearer" + ' ' + token
  return config;
}, 
  function (error){
  return Promise.rejest(error);
});

service.interceptors.response.use(function (response) {
  // 对响应数据做点什么
  return response;
}, function (error) {
  // 对响应错误做点什么
  return Promise.reject(error);
});

export default service