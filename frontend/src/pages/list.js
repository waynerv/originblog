import React, { useEffect } from 'react';
import styled from 'styled-components';
import { List } from 'antd';
import { useStores } from '../stores'
import { observer } from 'mobx-react';
import showdown from 'showdown';
import 'antd/dist/antd.css';

const Lists = styled.div`
padding: 0 50px;
`

const Component = observer(() => {
  const { ListStore } = useStores()
  useEffect(() => {
    ListStore.setQuery()
    if(ListStore.hasMore) ListStore.Find().then((data)=>{
      let $$Titles = document.querySelectorAll('.title')
      $$Titles.forEach(($node)=>{
        let index = [...$$Titles].indexOf($node)
        function TitleClick(){
          ListStore.setid(data[index].id)
          ListStore.Read().then((result)=>{
            $$Titles[index].href = document.location + '/' + data[index].id
          })
         
        }
        $node.addEventListener('click', TitleClick )
        $node.addEventListener('ready', ()=>{
          let converter = new showdown.Converter()
        document.body.innerHTML = converter.makeHtml(data[index].content)
        })
      })
    })
    //return ()=> ListStore.reset()
  });


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