import {Post, Request,Delete, Update} from './ajax';

const Blog = {
  // Publish(formData){
  //   return new Promise((resolve,reject) =>{
  //     Post('http://127.0.0.1:4523/mock/349959/api/posts', {formData}, (data)=>{console.log(data)}, (err)=>{console.log(err)})
  //     .then(data=> resolve(data))
  //      .catch(err=> reject(err))
  //    })
  // },
  // Update(post_id,formData){
  //   return new Promise((resolve,reject) =>{
  //     Update("http://127.0.0.1:4523/mock/349959/api/posts/%253Cpost_id%253E", post_id, formData, (data)=>{console.log(data)}, (err)=>{console.log(err)})
  //     .then(data=> resolve(data))
  //      .catch(err=> reject(err))
  //    })
  // },

  Find(query) {
    return new Promise((resolve, reject) =>{
      Request('http://81.68.174.36:8080/api/posts',{query}, ()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(Object.entries(data)[0][1])
        resolve(data)} )
       .catch(err=> reject(err))
    })
  },


  Read(post_id) {
    return new Promise((resolve, reject) =>{
      Request("http://81.68.174.36:8080/api/posts",{post_id}, ()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log('查看成功')
        resolve(data)} )
       .catch(err=> {
         alert('接口异常')
         reject(err)})
    })
  } 
}

const Categroy = {
  Find() {
    return new Promise((resolve,reject) => {
      Request("http://81.68.174.36:8080/api/categories",{},()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(data)
        resolve(data)} )
      .catch(err=> reject(err))
      })
    }
  
}


export {
  Blog,
  Categroy
}