import { observable, action } from 'mobx';
import { Categroy } from '../models';

class CategroyStore{
  @observable list =[]
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
        let newList = Object.entries(data)[0][1]
        this.append(newList);
        console.log(newList)
        resolve(newList)
        console.log('获取成功')
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
