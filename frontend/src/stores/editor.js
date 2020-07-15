import { observable, action } from 'mobx';

class EditorStore {
  @observable value = ''

  @action setValue(newValue){
    this.value = newValue
  }
  @action logout(){
    this.value = ''
  }
}

export default new EditorStore();