import React, { useEffect } from 'react';
import styled from 'styled-components';
import { List } from 'antd';
import { useStores } from '../stores'
import { observer } from 'mobx-react';

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
    <Lists>
       <List
        itemLayout="horizontal"
        dataSource={ListStore.list}
        renderItem={item => (
          <List.Item>
            <List.Item.Meta
              title= {item.title}
              description={item.summary}
            />
          </List.Item>
        )}
      />
    </Lists>
  )
})

export default Component;