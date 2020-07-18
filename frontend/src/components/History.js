import React from 'react';
import { Table, Tag, Space } from 'antd';

const Component = () => {
  const columns = [
    {
      title: 'Title',
      dataIndex: 'name',
      key: 'name',
      render: text => <a href='#'>{text}</a>,
    },
    
    {
      title: '发布日期',
      dataIndex: 'date',
      key: 'date',
      render: text => <p>{text}</p>,
    },
    
    {
      title: 'Tags',
      key: 'tags',
      dataIndex: 'tags',
      render: tags => (
        <>
          {tags.map(tag => {
            let color = tag.length > 5 ? 'geekblue' : 'green';
            if (tag === 'loser') {
              color = 'volcano';
            }
            return (
              <Tag color={color} key={tag}>
                {tag.toUpperCase()}
              </Tag>
            );
          })}
        </>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <a href='#'>Edit</a>
          <a href='#'>Delete</a>
        </Space>
      ),
    },
  ];
  
  const data = [
    {
      key: '1',
      name: '九种垂直居中',
      date: '2020/7/9',
      tags: ['nice', 'developer'],
    },
    {
      key: '2',
      name: 'Jim Green',
      date: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      date: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
  ];
  return(
    <div>
      <button>我的文章</button>
      <button>我的草稿</button>
      <input type="search" placeholder="搜索" />
      <Table columns={columns} dataSource={data} />
    </div>
  )
}

export default Component;