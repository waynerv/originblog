import {Post, Request,Delete, Update} from './ajax';
import UserStore from '../stores/User';

const Auth = {
  login(username, password) {
    return new Promise((resolve, reject) => {
      Post('http://127.0.0.1:4523/mock/349959/api/access-token',{username, password}, (data)=>{}, ()=>{console.log('接口异常')})
      .then(loginedUser=>{
        resolve(loginedUser)},error=> {
          reject(error)
        });
    });
  },

  logout() {
    localStorage.removeItem('token')
  }, 

  getCurrentUser() {
      return Request("http://127.0.0.1:4523/mock/349959/api/users/me", {}, ()=>{}, (err)=>{alert('端口异常')})
        .then(response =>{
        UserStore.currentUser = response.name
    })
  },

}

const Blog = {
  Publish(formData){
    return new Promise((resolve,reject) =>{
      Post('http://127.0.0.1:4523/mock/349959/api/posts', {formData}, (data)=>{console.log(data)}, (err)=>{console.log(err)})
      .then(data=> resolve(data))
       .catch(err=> reject(err))
     })
  },
  Update(post_id,formData){
    return new Promise((resolve,reject) =>{
      Update("http://127.0.0.1:4523/mock/349959/api/posts/%253Cpost_id%253E", post_id, formData, (data)=>{console.log(data)}, (err)=>{console.log(err)})
      .then(data=> resolve(data))
       .catch(err=> reject(err))
     })
  },

  Find(query) {
    return new Promise((resolve, reject) =>{
      Request('http://127.0.0.1:4523/mock/349959/api/posts',{query}, ()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(Object.entries(data)[0][1])
        resolve(data)} )
       .catch(err=> reject(err))
    })
  },

  Delete(post_id) {
    return new Promise((resolve, reject) =>{
      Delete('http://127.0.0.1:4523/mock/349959/api/posts',{post_id}, ()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(data)
        resolve(data)} )
       .catch(err=> {
         alert('接口异常')
         reject(err)})
    })
  },

  Read(post_id) {
    return new Promise((resolve, reject) =>{
      Request("http://127.0.0.1:4523/mock/349959/api/posts/%253Cpost_id%253E",{post_id}, ()=>{}, (err)=>{console.log(err)})
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
      Request("http://127.0.0.1:4523/mock/349959/api/categories",{},()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(data)
        resolve(data)} )
      .catch(err=> reject(err))
      })
    },

  Create(data) {
    return new Promise ((resolve,reject) => {
      Post('http://127.0.0.1:4523/mock/349959/api/categories', data, ()=>{}, ()=>{})
      .then(result => resolve(result))
      .catch(err => reject(err))
    })
  },

  Update(id, data) {
    return new Promise ((resolve,reject) => {
      Update('http://127.0.0.1:4523/mock/349959', id, data, ()=>{}, ()=>{})
      .then(result => resolve(result))
      .catch(err => reject(err))
    })
  },

  Delete(id) {
    return new Promise((resolve, reject) =>{
      Delete('http://127.0.0.1:4523/mock/349959/api/categories',id, ()=>{}, (err)=>{console.log(err)})
      .then(data=>{
        console.log(data)
        resolve(data)} )
       .catch(err=> {
         alert('接口异常')
         reject(err)})
    })
  },
  
}


export {
  Auth,
  Blog,
  Categroy
}