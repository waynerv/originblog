import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import 'antd/dist/antd.css';
import styled from 'styled-components'
import {useStores} from '../stores';
import { useHistory } from "react-router-dom";
import { observer } from 'mobx-react'
import { Login } from '../models/api.js'

const XLogin = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #001529;
`

const StyledForm = styled(Form)`
  max-width: 600px;
  margin: 70px auto;
  padding: 50px;
  border-radius: 8px;
  background: #fff;
`
const Component = observer(() => {
  const history = useHistory();
  const { AuthStore } = useStores();
  
  const onFinish = (value) => {
    let formData = new FormData()
    formData.append("username", value.username)
    formData.append("password", value.password)
    //AuthStore.setValues(formData);
    AuthStore.login(formData).then((result)=>{
      history.push('/view');
    }).catch((err)=> {
      console.log(err)
      message.error('登录失败')
    })
  };

  const onFinishFailed= error => {
    message.error(error)
  };
  
  return (
    <XLogin>
      <StyledForm
      id = "formData"
      name="normal_login"
      className="login-form"
      initialValues={{ remember: true }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
      <Form.Item
        name="username"
        rules={[{ required: true, message: 'Please input your Username!' }]}
      >
        <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="用户名" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[{ required: true, message: 'Please input your Password!' }]}
      >
        <Input
          prefix={<LockOutlined className="site-form-item-icon" />}
          type="password"
          placeholder="密码"
        />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" className="login-form-button">
          登录
        </Button>
      </Form.Item>
      <Form.Item>
        <a className="login-form-forgot" href="#">
          Forgot password
        </a>
      </Form.Item>
    </StyledForm>
  </XLogin>

  )
});

export default Component;