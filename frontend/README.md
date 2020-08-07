# My Blog

## 页面规划
> 分为前台和后台两部分，前台主要由上传列表、根据时间排序的时间列表、个人介绍构成；
后台分为登录、编辑页面、上传历史、个人信息编辑页面。

## 项目详情
### 前台
#### header部分在不同页面的title要相应的更新
> 使用`mobx-react`的observer对header组件进行观察，通过`{children}`进行参数传递，代码如下：

```jsx
import { observer } from 'mobx-react';

const Component = observer(({ imageObj , children }) =>{
  return (
    <Header>
      <h2>{children}</h2>
      <div className="second">
        <h4>Records Of Lainey</h4>
        <NavLink to='/' exact>首页</NavLink>
        <NavLink to='/history'>我的足迹</NavLink>
        <NavLink to='/about'>关于我</NavLink>
      </div>
    </Header>
  )
})
```

#### 不同页面的header背景图片动态更新
- 方法一：创建不同背景的首部js文件，在相应的组件中分别引入。
- 方法二：使用`styled components`通过参数传递背景图片地址
```jsx
import styled from 'styled-components';

const Header = styled.div`
  height: 100vh;
  width: 100%;
  box-sizing: border-box;
  background: url(${props => props.imgUrl}) no-repeat center;
  background-size: cover;
  ...
//一定要记得将`...props`作为参数传入，否则url为空
  const Component = observer(({ children , ...props}) =>{
  return (
    <Header {...props}> 
      <h2>{children}</h2>
    </Header>
`
```

在使用组件时设置图片地址（可以是本地图片引入也可以是线上地址）
```jsx
import image1 from '../images/home-bg.jpg';

const Component = () => {
  return (
    <Home>
      <Header imgUrl={`${image1}`}>提交列表</Header>
    //  <Header imgUrl="https://i.loli.net/2020/07/07/XUzwaReJL2WCrc8.jpg" /> 
      <List />
    </Home>
  )
}
```