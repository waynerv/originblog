import React from 'react';
import MarkdownIt from 'markdown-it';
import MDEditor from '@uiw/react-md-editor';
import styled from 'styled-components';

const ButtonGloup = styled.div`
  margin-top: 15px;
  margin-left: 15px;
`

const Button = styled.button`
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

//  const title3: ICommand ={
//   TextareaHTMLAttributes: {resize: 'none' },
//   height: {number: '500'},

 const Component = () => {
  const [value, setValue] = React.useState("**Hello world!!!**");
  return (
    <div className="container">
      <MDEditor
        value={value}
        onChange={setValue}
        height='90vh'
        visiableDragbar = 'false'
      />
      {/* <MDEditor.Markdown source={value} /> */}
      <ButtonGloup className="button">
        <Button>保存</Button>
        <Button>提交</Button>
      </ButtonGloup>
    </div>
  );
}

export default Component;