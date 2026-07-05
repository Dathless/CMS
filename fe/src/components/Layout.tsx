import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { Layout, Menu, Button, Typography } from "antd";
import {
  DashboardOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  SunOutlined,
  MoonOutlined,
} from "@ant-design/icons";
import { useAuth } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";

const { Header, Sider, Content } = Layout;

export default function AppLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const { user, logout } = useAuth();
  const { mode, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const menuItems = [
    {
      key: "/",
      icon: <DashboardOutlined />,
      label: "Dashboard",
    },
    {
      key: "/profile",
      icon: <UserOutlined />,
      label: "Profile",
    },
  ];

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div
          style={{
            height: 32,
            margin: 16,
            color: "white",
            textAlign: "center",
            fontWeight: "bold",
            fontSize: collapsed ? 12 : 14,
          }}
        >
          {collapsed ? "CMS" : "Course Management"}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["/"]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: "0 24px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
          />
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <Button
              type="text"
              icon={mode === "dark" ? <SunOutlined /> : <MoonOutlined />}
              onClick={toggleTheme}
            />
            <Typography.Text>
              {user?.full_name} ({user?.role})
            </Typography.Text>
            <Button type="text" icon={<LogoutOutlined />} onClick={logout}>
              Logout
            </Button>
          </div>
        </Header>
        <Content style={{ margin: 24, padding: 24, minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
