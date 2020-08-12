import React, { useEffect } from 'react';
import styled from 'styled-components';
import Header from '../components/header';
import image2 from '../images/history-bg.jpg';
import { useStores } from '../stores';
import { observer } from 'mobx-react';
import Timeline from './timeline';

const Lists = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`
const Component = observer(() => {
  const { ListStore } = useStores()
  useEffect(() => {
    ListStore.setQuery()
    if(ListStore.hasMore) ListStore.Find()
    //return ()=> ListStore.reset()
  });
  return (
    <>
      <Header imgUrl={`${image2}`}>我的历程</Header>
      <Lists>
        <Timeline/>
      </Lists>
    </>
  )
})

export default Component;