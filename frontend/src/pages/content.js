import React, { useEffect } from 'react';
import styled from 'styled-components';
import { useStores } from '../stores'
import { observer } from 'mobx-react';
import showdown from 'showdown';


const Lists = styled.div`
padding: 0 50px;
`

const Component = observer(() => {
  const { ListStore } = useStores()
  let converter = new showdown.Converter()
  document.querySelector('#text').innerHTML = converter.makeHtml(ListStore.content)

  return (
  <>
    <h1>{ListStore.title}</h1>
    <div id="text"></div>
  </>
  )
})

export default Component;