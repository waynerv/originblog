import React, { useEffect } from 'react';
import styled from 'styled-components';
import { List } from 'antd';
import { useStores } from '../stores'
import { observer } from 'mobx-react';
import { useHistory } from "react-router-dom";
import 'antd/dist/antd.css';

const Lists = styled.div`
padding: 0 50px;
`

const Component = observer(() => {
  const history = useHistory();
  const { ListStore } = useStores()
  useEffect(() => {
    ListStore.setQuery()
    if(ListStore.hasMore) ListStore.Find().then(()=>{
      let $$Titles = document.querySelectorAll('.title')
      $$Titles.forEach(($node)=>{
        let index = [...$$Titles].indexOf($node)
        // $$Titles[index].href = document.location + ListStore.list[index].slug
        $node.addEventListener('click', ()=>{
          ListStore.setid(ListStore.list[index].id)
          ListStore.Read().then((response)=>{
            // ListStore.setTitle(response.title)
            // ListStore.setContent(response.content)
            ListStore.setTitle('标题')
            ListStore.setContent('内容有很多')
            history.push('/content')
          })
        })
      })
        
    })
  })


  return (
  <Lists>
    <List
    itemLayout="horizontal"
    dataSource={ListStore.list}
    renderItem={item => (
      <List.Item>
        <List.Item.Meta
          title= {<a className='title' target="_blink" >{item.title}</a>}
          description={item.summary}
        />
      </List.Item>
    )}
    />
  </Lists>
  )
})

export default Component;