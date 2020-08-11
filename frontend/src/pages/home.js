import React from 'react';
import styled from 'styled-components';
import List from './list';
import Header from '../components/header';
import image1 from '../images/home-bg.jpg';

const Home = styled.div`
  width: 100%;
  margin: 0;
`;


const Component = () => {
  return (
    <Home>
      <Header imgUrl={`${image1}`}>文章列表</Header>
      <List />
    </Home>
  )
}

export default Component;