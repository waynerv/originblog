import React from 'react';
import { Menu, Table,  Space} from 'antd';
import styled from 'styled-components';
import { useStores } from '../stores';
import { observer } from 'mobx-react';

const Form = styled.form`
  display: flex;
  flex-wrap: wrap-reverse;
  align-items: center;
  justify-content: space-evenly;
  margin: 10px 10px;
  padding: 10px 0;
  `

const Textarea = styled.textarea`
  width: 200px;
  height: 2em;
  resize: none;
`
const Input = styled.input`
border-radius: 6px;
outline: none;
background: #fff;
border: 1px solid #ddd;
cursor: pointer;
&:hover{
  border: 1px solid #1890FF;
  color: #1890FF;
};

&:active{
  color: #fff;
  background: #1890ff;
}
`

const Component = observer(() => {
  const { PostStore } = useStores()
  function handSubmit(e){
    e.preventDefault()
    const $ = s => document.querySelector(s)
    const $form = $('.operation')
    PostStore.setQuery($form)
    PostStore.Find().then((data)=> {
      console.log(data)
    })
    .catch((err)=>{
      console.log(err)
      console.log('fabushibai')
    })
    
  }
  
  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: text => <a href='#'>{text}</a>,
    },
    
    {
      title: '发布日期',
      dataIndex: 'date',
      key: 'date',
      render: text => <p>{text}</p>,
    },
    
    {
      title: '简介',
      key: 'summary',
      dataIndex: 'summary',
      render: text => <p>{text}</p>
    },
        
    {
      title: '操作',
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
      key: PostStore.list,
      title: '九种垂直居中',
      date: '2020/7/9',
      summary: '',
    },
    {
      key: '2',
      title: 'Jim Green',
      date: 'London No. 1 Lake Park',
      summary: '',
    },
    {
      key: '3',
      title: 'Joe Black',
      date: 'Sidney No. 1 Lake Park',
      summary: '',
    },
  ];
  
  return(
    <div>
      <Form className='operation' onSubmit={handSubmit}>
        标题:<Textarea placeholder="请输入标题" name="title"/>
        标签:<Textarea placeholder="请输入标签" name="tag"/> 
        文章分类:
        <select name="categroy_id">
          <option>文章</option>
          <option>技术</option>
          <option>记录</option>
        </select>
        是否显示草稿：
        <select name="is_draft">
          <option value="true">是</option>
          <option value="false"> 否</option>
        </select>
        <Input type="submit" value="查询" />
        <Input type="reset" />
      </Form>
      <Table columns={columns} dataSource={data} />
    </div>
  )
})

export default Component;