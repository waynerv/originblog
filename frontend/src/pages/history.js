import React from 'react';
import styled from 'styled-components';
import Header from '../components/header';
import {
  Timeline,
  Content,
  ContentYear,
  ContentBody,
  Description
} from 'vertical-timeline-component-react';
import image2 from '../images/history-bg.jpg';

const List = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`
const Component = () => {
 
  return (
    <>
      <Header imgUrl={`${image2}`}>我的历程</Header>
      <List>
      <Timeline>
        <Content>
          <ContentYear
            startMonth="07"
            monthType="text"
            startDay="03"
            startYear="2020"
            currentYear
          />
          <ContentBody title="垂直居中">
            <Description
              text="I'm an amazing event"
              optional="I'm an amazing optional text"
            />
          </ContentBody>
        </Content>
        <Content>
          <ContentYear
            startMonth="07"
            monthType="text"
            startDay="04"
            startYear="2020"
            currentYear
          />
          <ContentBody title="原型链">
            <Description
              text="I'm an amazing event"
              optional="I'm an amazing optional text"
            />
          </ContentBody>
        </Content>
        <Content>...</Content>
      </Timeline>
      </List>
    </>
  )
}

export default Component;