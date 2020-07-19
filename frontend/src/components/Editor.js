import React, { useState } from 'react';
// import MarkdownIt from 'markdown-it';
import MDEditor from '@uiw/react-md-editor';
import styled from 'styled-components';
import { useStores } from '../stores';
import { observer } from 'mobx-react';
import {  message } from 'antd';



const ButtonGloup = styled.div`
  margin-top: 15px;
  margin-left: 15px;
`

const Input = styled.input`
  padding: 5px;
  margin-left: 15px;
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
const Textarea = styled.textarea`
  display: block;
  resize: none;
  width: 100%;
  border: none;
  font-size: 30px;
  line-height: 1;
  font-weight: 600;
`

const Summary = styled.textarea`
  display: block;
  resize: none;
  width: 100%;
  border: none;
  border-top: 1px solid #ddd;
`
const Component = observer(() => {
  const { PostStore } = useStores()
  const [ form, setForm ] = useState({title:'', slug: '',summar:''})
  function Check() {
    if (form.title.length> 30) {
      message.error('标题最多30个字')
    }
    if(/[^A-Za-z0-9\s]/.test(form.slug)){
      message.error('英文标题必须由字母组成')
    }else return true 
  }

  function handSubmit(e){
    e.preventDefault()
    const $ = s => document.querySelector(s)
    const $form = $('#editor')
    const $msg = $('#msg')
    PostStore.setFormData($form)
    if(Check()){
      PostStore.Publish().then((data)=> {
        console.log(data)
        $msg.innerText = data.msg
      })
      .catch((err)=>{
        console.log(err)
        console.log('fabushibai')
        $msg.innerText = '接口异常' 
      })
    }
  }
  

  return (
    <form id="editor" action='http://127.0.0.1:4523/mock/349959/api/posts'  method='POST' onSubmit={handSubmit}>
      <Textarea 
      name="title" 
      value={form.title} 
      onChange={e => setForm({...form, title:e.target.value})} placeholder="请输入标题(最多30个字)"
      />
      <Summary 
      name="slug" 
      value={form.slug} 
      onChange={e => setForm({...form, slug:e.target.value})} placeholder="请输入英文标题" 
      required
      />
      <Summary 
      name="summary" 
      value={form.summary} 
      onChange={e => setForm({...form, summary:e.target.value})} 
      placeholder="请输入摘要"
      />
      <textarea 
      name="content"  
      value={PostStore.content} 
      hidden readOnly
      />

      <MDEditor
        id="msg"
        name="content"
        value={PostStore.content}
        onChange={() => PostStore.setContent()}
        height='90vh'
      />
  
      
      {/* <MDEditor.Markdown source={value} /> */}
      <ButtonGloup className="button">
        <Input type="checkbox" name="is_draft"/>保存成草稿
        <Input type="submit" />
      </ButtonGloup>
    </form>
  );

})

export default Component;