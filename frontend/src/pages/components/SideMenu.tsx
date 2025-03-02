import React from 'react';
import { Layout, Menu } from 'antd';
import { items } from '../../constants/menuItems'; // Itens do menu extraídos

const { Sider } = Layout;

interface SideMenuProps {
    collapsed: boolean;
    onCollapse: (value: boolean) => void;
}

const SideMenu: React.FC<SideMenuProps> = ({ collapsed, onCollapse }) => {
    return (
        <Sider collapsible collapsed={collapsed} onCollapse={onCollapse} style={{ paddingTop: 16 }}>
            <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items} />
        </Sider>
    );
};

export default SideMenu;