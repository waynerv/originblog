import { observable, action, toJS } from 'mobx';
import { Categroy } from '../models';

class CategroyStore{
  @observable list =[]
  //categroylist = toJS(this.list) 将观察对象数据转换成js数组
  @observable AddItem = ''
  @observable id = ''
  
  @action append(newList){
    this.list = this.list.concat(newList)
  }
  @action setAddItem(newItem){
    this.AddItem = newItem
  }
  @action setid(id){
    this.id = id
  }

  @action Find() {
    return new Promise((resolve, reject) => {
      Categroy.Find().then(data => {
        this.append(data);
        console.log(toJS(this.list))
        resolve(data)
      }).catch(err => {
        reject(err)
        console.log('获取失败')
      })
    })
  }

  @action Create() {
    return new Promise((resolve, reject) => {
      Categroy.Create(this.AddItem).then(() => {
        this.append(this.AddItem);
        resolve()
        console.log('目录创建成功')
      }).catch(err => {
        reject(err)
        console.log('目录创建失败')
      })
    })
  }
  @action Update() {
    return new Promise((resolve, reject) => {
      Categroy.Update(this.AddItem).then(() => {
        this.append(this.AddItem);
        resolve()
        console.log('目录创建成功')
      }).catch(err => {
        reject(err)
        console.log('目录创建失败')
      })
    })
  }

  @action Delete() {
    return new Promise((resolve, reject) => {
      Categroy.Delete(this.id).then(() => {
        resolve()
        console.log('删除成功')
      }).catch(err => {
        reject(err)
        console.log('删除失败')
      })
    })
  }

  @action reset() {
    
  }

}

export default new CategroyStore();
