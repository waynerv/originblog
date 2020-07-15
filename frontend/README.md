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
