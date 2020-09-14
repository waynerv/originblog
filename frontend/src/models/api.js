import service from './request.js';


  function Login(data){
    return service.request({
      url: "http://81.68.174.36:8080/api/auth/access-token",
      method: "post",
      data
    })
  } 

  function Find(data){
    
    return service.request({
      url: "http://81.68.174.36:8080/api//api/posts",
      method: "get",
      params: data,
    })
  } 

  function Publish(data){
    return service.request({
      url: "http://81.68.174.36:8080/api/posts",
      method: "post",
      data,
    })
  }   
export {
  Login,
  Find,
  Publish
}