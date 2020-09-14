import React from 'react';
import { Table,  Space, Button, message} from 'antd';
import styled from 'styled-components';
import { useStores } from '../stores';
import { observer } from 'mobx-react';
import { useHistory, Link } from "react-router-dom";

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
  const { PostStore, CategroyStory } = useStores()
  const history = useHistory();

  function handSubmit(e){
    e.preventDefault()
    const $ = s => document.querySelector(s)
    const $form = $('.operation')
    PostStore.setQuery($form)
    PostStore.find().then((data)=> {
      console.log("获取成功")
    })
    .catch((err)=>{
      console.log(err)
      console.log('获取失败')
    })
  };


  const handClick = item =>{ 
    PostStore.setid(item.key)
    let index = (PostStore.list).findIndex(arr => arr.id=== item.key)
    PostStore.Delete().then(()=> {
      //console.log(index)找不到index
      PostStore.list.splice(index,1) 
    message.success('删除成功')
    }).catch((err)=>{
      console.log(err)
      message.error('删除失败')}
      )
  };
  const handEdit = key =>{
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

  
  
  function handCategroy (){
    let $Categroy = document.querySelector('#categroy_id')
    $Categroy.length = 0
    for (let i = 0; i < CategroyStory.list.length; i++) {
      let $option = document.createElement("option")
      $option.setAttribute = ('value',CategroyStory.list[i].id)
      $option.key = CategroyStory.list[i].id
      $option.innerText = CategroyStory.list[i].name
      $Categroy.appendChild($option)
  }
};
  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: text => <Link to='/view/article' target='_blank' onClick={handEdit}>{text}</Link>,
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
          <Button onClick={()=>handClick()}>删除</Button>
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
        <select name="categroy_id"  id="categroy_id" onClick={handCategroy}>
          <option value="-1" disabled>请选择</option>
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