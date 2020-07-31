import { observable, action} from 'mobx';
import { Auth } from '../models';

class UserStore {
 @observable currentUser=null;


 @action pullUser() {
  Auth.getCurrentUser()
}

@action resetUser() {
  this.currentUser = null;
}

}

export default new UserStore();