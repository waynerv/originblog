# Blog Opreation

## 项目介绍
本项目属于`my blog`项目的后台管理界面，主要功能：登录、发布历史查询、发布、个人信息设置。

## 项目记录
### 登录页面
使用`antd`组件的`form`表单, 针对`antd`组件的样式需要引入专门的样式，地址如下：
```js
import 'antd/dist/antd.css';
```
### 登录页面跳转到主页面的路由实现
因为登录页面不需要侧边栏.而主页面需要侧边栏作为公用组件;
创建`home.js`文件,在home.js中引入`<Nav>`组件以及各个页面组件,在`App.js`中引入`<Home>`组件,通过路由实现跳转.
**App.js**
```jsx
import Login from './pages/login';
import Home from './home';

function App() {
  return (
    <>
      <Switch>
        <Route path='/' exact component={Login} />
        <Route path='/view' component={Home} >
        </Route>
      </Switch>
</>
  )
}

```

**home.js**
```jsx
import Nav from './components/nav';
import Artic from './components/artic'

function Home() {
  return (
    <>
      <Nav />
      <main>
        <Suspense fallback={<div>Loading!!</div>}>
          <Switch>
            <Route path='/view/artic' component={Artic} />
            ...
          </Switch>
        </Suspense> 
      </main>
    </>
  )
}
```

### 二级路由的实现
1. 在当前页面的所在位置创建子文件夹,在子文件夹中创建新的js文件;
2. <Link to='/main/sub'>
3. 在main组件中需要的位置通过`<Route path='/main/sub' component={sub}/>`引入子组件
[参考链接](https://www.bilibili.com/video/BV1gE411W74U?p=6)

### 进入主页面后自动跳转到列表页
使用`<Redirect>`实现路由跳转
```jsx
<Redirect from='/view' to='/view/history'/>
```
## 状态管理
基于antd的form组件，使用mobx和mobx-react进行管理数据。
### 登录功能
创建新的stores数据管理文件夹，stores下添加Auth.js管理用户信息；
创建models文件夹管理接口和数据操作具体逻辑的实现。
```
src
  components
  + models
    + index.js
  public
  pages
  + stores
    + Auth.js
```
### AJAX的封装
```js
function Post (url, data, onsucceed, onfaill) {
   let xhr = new XMLHttpRequest();
   xhr.withCredentials = true;
   xhr.open("POST", url, true);
   xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
   xhr.onload = function() {
     if(xhr.status>=200 && xhr.status<300 || xhr.status===304){
      onsucceed(JSON.parse(xhr.responseText))
    }else {
       onfaill()
     }
    }
   xhr.send(data);
 }
```

在使用时会报错“TypeError cannot read property .then of undefined”，使用代码如下：
```js
login(username, password) {
    return new Promise((resolve, reject) => {
      Post('http://127.0.0.1:4523/mock/349959/api/access-token',{username, password}, ()=>{console.log(username)}, ()=>{console.log('接口异常')})
      .then(loginedUser=>{
        resolve(loginedUser)},error=> {
          reject(error)
        });
    });
  },
```

解决办法：在封装AJAX时需要return new Promise
```js
return new Promise((resolve,reject) =>{
    let xhr = new XMLHttpRequest();
  xhr.withCredentials = true;
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.onload = function() {
    if(xhr.status>=200 && xhr.status<300 || xhr.status===304){
      onsucceed(resolve(JSON.parse(xhr.responseText)))
    }else {
      onfaill(err=>reject(err))
    }
  }
  xhr.send(data);
  }) 
}
```

### form表单提交信息不包含`<Editor>`组件的内容
解决办法：插入一个`<textarea name="content" value={PostStore.content} hidden readOnly />`,具体内容的控制是由`<Editor>`组件的`value`和`onChanag`事件控制。
### form表单提交未进入提交函数
需要在函数第一行添加`e.preventDefault`

### antd table 报错如下：
> Warning: [antd: Table] Each record in dataSource of table should have a unique `key` prop, or set `rowKey` of Table to an unique primary key.

- 解决办法一： 给datasouce中的每一项第一个添加一个key
``` js
const dataSource = [{
  key: '1',
  name: '胡彦斌',
  age: 32,
  address: '西湖区湖底公园1号'
}, {
  key: '2',
  name: '胡彦祖',
  age: 42,
  address: '西湖区湖底公园1号'
}];
```

- 解决办法二：设置rowKey,返回的是数据中的唯一值
```jsx
<Table columns={columns} dataSource={PostStore.list} rowKey={record => record.id}/> 
```