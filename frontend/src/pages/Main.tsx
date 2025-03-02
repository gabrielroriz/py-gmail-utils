import React, { useState, useEffect } from 'react';

import {
    DesktopOutlined,
    MailOutlined,
} from '@ant-design/icons';

import type { MenuProps } from 'antd';

import { Breadcrumb, Layout, Menu } from 'antd';
import useApi from '../hooks/useApi.hook';
import GmailLikeList from './components/GmailLikeList';

const { Content, Footer, Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

function getItem(
    label: React.ReactNode,
    key: React.Key,
    icon?: React.ReactNode,
    children?: MenuItem[],
): MenuItem {
    return {
        key,
        icon,
        children,
        label,
    } as MenuItem;
}

const items: MenuItem[] = [
    getItem('Gmail', '1', <MailOutlined />),
    getItem('Option 2', '2', <DesktopOutlined />),
    getItem('User', 'sub1', <DesktopOutlined />, [
        getItem('Tom', '3'),
        getItem('Bill', '4'),
        getItem('Alex', '5'),
    ]),
];

const Main: React.FC = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [data, setData] = useState([]);

    const { getMails } = useApi();

    useEffect(() => {
        const requestMails = async () => setData(await getMails({ max_results: 250 }))
        requestMails()
    }, [])

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)} style={{ paddingTop: 16 }}>
                <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items} />
            </Sider>
            <Layout>
                <Content style={{ margin: '0 16px' }}>
                    <Breadcrumb style={{ margin: '16px 0' }}>
                        <Breadcrumb.Item>User</Breadcrumb.Item>
                        <Breadcrumb.Item>Bill</Breadcrumb.Item>
                    </Breadcrumb>
                    <div style={{ padding: 24, minHeight: 360 }}>
                        <GmailLikeList data={data} />
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Ant Design ©{new Date().getFullYear()} Created by Ant UED
                </Footer>
            </Layout>
        </Layout >
    );
};

export default Main;