import { observable, action } from 'mobx';
import { Blog } from '../models';
import { Find, Publish } from '../models/api';

class PostStore{
  @observable page = 0;
  pre_page = 20;
  @observable formData = {}
  @observable list =[]
  @observable query = {}
  @observable hasMore = true
  @observable id = ''
  @observable values = {
    title:'',
    slug:'',
    summary:'',
    content:'# Hello'
  }

  @action setContent(newContent){
    this.values.content = newContent
  };
  @action setTitle(newTitle){
    this.values.title = newTitle
  };
  @action setSlug(newSlug){
    this.values.slug = newSlug
  };
  @action setSummary(newSummary){
    this.values.summary = newSummary
  };

  @action setFormData(newFormData){
    this.formData = newFormData
 
  };

  @action setQuery($dom){
    this.query = new FormData($dom)
    this.query.append(this.page, this.per_page)
    this.query.serialize()
  };
  @action append(newList){
    this.list = this.list.concat(newList)
  }
  @action setid(newId){
    this.id = newId
  }

  @action publish(data) {
    return new Promise((resolve, reject) => {
      Publish(data).then(date => {
        resolve(date)
        console.log('发布成功')
      }).catch(err => {
        reject(err)
        console.log('发布失败')
      })
    })
  }
  @action Update() {
    return new Promise((resolve, reject) => {
      Blog.Update(this.id,this.formData).then(date => {
        resolve(date)
        console.log('gengx成功')
      }).catch(err => {
        reject(err)
        console.log('gengx失败')
      })
    })
  }

  //JSON.parse(JSON.stringify(res.data))
  @action find() {
    this.hasMore = true;
    return new Promise((resolve, reject) => {
      Find(this.formData).then(data => {
        let newList = Object.entries(data)[0][1]
        this.append(newList);
        this.page++
        //console.log(newList)
        resolve(data)
        if(newList.length < this.pre_page) {
          this.hasMore = false
        }
        console.log('获取成功')
      }).catch(err => {
        reject(err)
        console.log(err)
      })
    })
  }

  @action Delete() {
    return new Promise((resolve, reject) => {
      Blog.Delete(this.id).then(() => {
        resolve()
        console.log('删除成功')
      }).catch(err => {
        reject(err)
        console.log('删除失败')
      })
    })
  }

  @action Read() {
    return new Promise((resolve, reject) => {
      Blog.Read(this.id).then(() => {
        resolve()
        console.log('查询成功')
      }).catch(err => {
        reject(err)
        console.log('查询失败')
      })
    })
  }

  @action reset() {
    this.content = '# hello'
    this.formData = {}
    this.query ={}
    this.page = 0;
    this.list = [];
    this.hasMore = true;
  }

}

export default new PostStore();
