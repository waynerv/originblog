import React from 'react';
import { Menu, Button } from 'antd';
import { Link } from 'react-router-dom';
import {
  AppstoreOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  PieChartOutlined,
  DesktopOutlined,
  ContainerOutlined,
  MailOutlined,
} from '@ant-design/icons';

const { SubMenu } = Menu;

class Nav extends React.Component {
  state = {
    collapsed: false,
  };

  toggleCollapsed = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  };

  render() {
    return (
      <nav style={{ width: 256 }}>
        <Button type="primary" onClick={this.toggleCollapsed} style={{ marginBottom: 16 }}>
          {React.createElement(this.state.collapsed ? MenuUnfoldOutlined : MenuFoldOutlined)}
        </Button>
        <Menu
          defaultSelectedKeys={['1']}
          defaultOpenKeys={['sub1']}
          mode="inline"
          theme="dark"
          inlineCollapsed={this.state.collapsed}
        >
          <Menu.Item key="1" icon={<ContainerOutlined />}>
          <Link to='/view/history'>博客列表</Link>
          </Menu.Item>
          <SubMenu key="sub1" icon={<AppstoreOutlined />} title="我的博客">
            <Menu.Item key="2"> <Link to='/view/editor'>编辑</Link></Menu.Item>
          </SubMenu>
          <SubMenu key="sub2" icon={<DesktopOutlined />} title="个人信息">
            <Menu.Item key="4"><Link to='/view/information'>信息编辑</Link></Menu.Item>
          </SubMenu>
        </Menu>
      </nav>
    );
  }
}

export default Nav;