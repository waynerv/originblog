import React from 'react';
import { Table,  Space, Button, message} from 'antd';
import styled from 'styled-components';
import { useStores } from '../stores';
import { observer } from 'mobx-react';
import { useHistory } from "react-router-dom";

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
  const history = useHistory();

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
  };


  const handClick = key =>{ 
    PostStore.setid(key)
    let index = (PostStore.list).findIndex(arr => arr.id=== key)
    PostStore.Delete().then(()=> {
      //console.log(index)找不到index
      PostStore.list.splice(index,1) 
    message.success('删除成功')
    }).catch((err)=>{
      console.log(err)
      message.error('删除失败')}
      )
  };
  const handEdit = (key) =>{
    PostStore.setid(key)
    PostStore.Read().then((result)=> {  
      console.log(result)
      //console.log(index)找不到index
      PostStore.setTitle(result.title)
      PostStore.setSlug(result.slug)
      PostStore.setSummary(result.summary)
      PostStore.setContent(result.content)
      history.push('/view/update')
    }).catch((err)=>{
      console.log(err)
  })  
};
  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: text => <a href='#'>{text}</a>,
    },
    
    {
      title: '发布日期',
      dataIndex: 'created_at',
      key: 'created_at',
      render: text => <p>{text}</p>,
    },
    
    {
      title: '简介',
      key: 'summary',
      dataIndex: 'summary',
      render: text => <p>{text}</p>
    },
    {
      title: '标签',
      key: 'tag_names',
      dataIndex: 'tag_names',
      render: text => <p>{text}</p>
    },
        
    {
      title: '操作',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button onClick={()=>handEdit(record.key)}>编辑</Button>
          <Button onClick={()=>handClick(record.key)}>删除</Button>
        </Space>
      ),
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
      <Table columns={columns} dataSource={PostStore.list} rowKey={record => record.id}/>  
    </div>
  )
})

export default Component;