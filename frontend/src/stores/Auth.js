import { observable, action} from 'mobx';
import { Auth } from '../models/index';
import UserStore from './User';
import PostStore from './Post';
import CategroyStory from './categroy';

class AuthStore{
  @observable values = {
    username: '',
    password: ''
  };
 
  @action setUsername(username) {
    this.values.username = username
  }

  @action setPassword(password) {
    this.values.password = password
  }

  @action login(){
    return new Promise((resolve, reject) =>{
      Auth.login(this.values.username, this.values.password).then(user=>{
        UserStore.pullUser();
        PostStore.Find();
        CategroyStory.Find();
        resolve(user);
      }).catch(err=>{
        UserStore.resetUser();
        console.log(err)
        reject(err);
      })
    });
  };

  @action logout() {
    Auth.logout();
    UserStore.resetUser();
  }
}

export default new AuthStore()
