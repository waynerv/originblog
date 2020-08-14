import React from 'react';
import { NavLink } from 'react-router-dom';
import { observer } from 'mobx-react';
import styled from 'styled-components';


const Header = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
  box-sizing: border-box;
  color: #fff;
  font-size: 30px;
  background: url(${props => props.imgUrl}) no-repeat center;
  background-size: cover;
  
  &::after{
    content:'';
    width: 100%;
    height: 100%;
    display: block;
    background-color: rgba(0,0,0, 0.3);
  }
  .second{
    position: absolute;
    top: 20px;
    left: 0;
    width: 100%;
    display: flex;
    align-items: center;
    font-size: 16px;

    h4{
      margin: 0;
      flex: 1;
      font-size: 1.5em;
    }

    a {
      color: #fff;
      text-decoration: none;
      margin-right: 1em;
    }
    a:hover {
      color: #ddd;
    } 
  }
  
  h2{
    position: absolute;
  }
`

const Component = observer(({ children , ...props}) =>{
  return (
    <Header {...props}> 
      <h2 style={{color:'#fff'}}>{children}</h2>
      <div className="second">
        <h4 style={{color:'#fff'}}>Records Of Lainey</h4>
        <NavLink to='/' exact>首页</NavLink>
        <NavLink to='/history'>我的足迹</NavLink>
        <NavLink to='/about'>关于我</NavLink>
      </div>
    </Header>
  )
})

export default Component;