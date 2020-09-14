import { observable, action} from 'mobx';
import { Login } from '../models/api.js';
import UserStore from './User';
import PostStore from './Post';
import CategroyStory from './categroy';

class AuthStore{

  @action login(data){
    return new Promise((resolve, reject) =>{
      Login(data).then(res=>{
        console.log(res)
        window.localStorage.setItem('token', res.data.access_token)
        console.log( res.data.access_token)
        //UserStore.pullUser();
        PostStore.find();
        CategroyStory.Find();
        resolve(res);
      }).catch(err=>{
        UserStore.resetUser();
        console.log(err)
        reject(err);
      })
    });
  };

  @action logout() {
    //Auth.logout();
    UserStore.resetUser();
  }
}

export default new AuthStore()
