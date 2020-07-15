import React from 'react';
import { Form, Input, Button, Checkbox } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import 'antd/dist/antd.css';
import styled from 'styled-components'

const Login = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #001529;
`
const StyledForm = styled.div`
  max-width: 600px;
  margin: 70px auto;
  padding: 50px;
  border-radius: 8px;
  background: #fff;
`
  const Component = () => {
      const onFinish = values => {
        console.log('Received values of form: ', values);
      };
  
  return (
    <Login>
      <StyledForm
      name="normal_login"
      className="login-form"
      initialValues={{ remember: true }}
      onFinish={onFinish}
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
        </Button>&nbsp;&nbsp;&nbsp;&nbsp;
        <Button type="primary" htmlType="submit" className="forget-password-button">
            忘记密码
          </Button>
      </Form.Item>
      <Form.Item>
        
        {/* <a className="login-form-forgot" href="">
          Forgot password
        </a> */}
      </Form.Item>
    </StyledForm>
  </Login>
  )
};

export default Component;