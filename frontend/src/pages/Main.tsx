// import React, { useState, useEffect, useRef } from 'react';
// import { DesktopOutlined, MailOutlined } from '@ant-design/icons';
// import type { MenuProps } from 'antd';
// import { Breadcrumb, Layout, Menu, Spin, Form, InputNumber, Button } from 'antd';
// import useApi from '../hooks/useApi.hook';
// import GmailLikeList from './components/GmailLikeList';

// const { Content, Footer, Sider } = Layout;

// type MenuItem = Required<MenuProps>['items'][number];

// function getItem(
//     label: React.ReactNode,
//     key: React.Key,
//     icon?: React.ReactNode,
//     children?: MenuItem[],
// ): MenuItem {
//     return {
//         key,
//         icon,
//         children,
//         label,
//     } as MenuItem;
// }

// const items: MenuItem[] = [
//     getItem('Gmail', '1', <MailOutlined />),
//     getItem('Option 2', '2', <DesktopOutlined />),
//     getItem('User', 'sub1', <DesktopOutlined />, [
//         getItem('Tom', '3'),
//         getItem('Bill', '4'),
//         getItem('Alex', '5'),
//     ]),
// ];

// const Main: React.FC = () => {
//     const [collapsed, setCollapsed] = useState(false);
//     const { loading, getMails } = useApi();
//     const hasFetched = useRef(false);

//     // 🔹 Obtém um parâmetro específico da URL
//     const getQueryParam = (param: string): number | null => {
//         const searchParams = new URLSearchParams(window.location.search);
//         const value = searchParams.get(param);
//         return value ? parseInt(value, 10) : null;
//     };

//     // 🔹 Estado para armazenar max_results (inicializa com o valor da URL ou padrão 250)
//     const [maxResults, setMaxResults] = useState(getQueryParam('max_results') || 250);
//     const [data, setData] = useState([]);

//     // 🔹 Atualiza a URL manualmente ao alterar max_results
//     const updateURL = (newMaxResults: number) => {
//         const searchParams = new URLSearchParams(window.location.search);
//         searchParams.set('max_results', newMaxResults.toString());
//         const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
//         window.history.replaceState(null, '', newUrl);
//     };

//     // 🔹 Função para buscar os e-mails ao clicar no botão
//     const fetchMails = async () => {
//         updateURL(maxResults); // Atualiza o valor na URL
//         setData(await getMails({ max_results: String(maxResults) }));
//     };

//     useEffect(() => {
//         if (hasFetched.current) return;
//         hasFetched.current = true;
//         fetchMails(); // Busca inicial com max_results da URL ou padrão
//     }, []);

//     return (
//         <Layout style={{ minHeight: '100vh' }}>
//             <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)} style={{ paddingTop: 16 }}>
//                 <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items} />
//             </Sider>
//             <Layout>
//                 <Content style={{ margin: '0 16px' }}>
//                     <Breadcrumb style={{ margin: '16px 0' }}>
//                         <Breadcrumb.Item>User</Breadcrumb.Item>
//                         <Breadcrumb.Item>Bill</Breadcrumb.Item>
//                     </Breadcrumb>

//                     {/* Formulário para definir max_results */}
//                     <Form layout="inline" style={{ marginBottom: 16 }}>
//                         <Form.Item label="Max Results">
//                             <InputNumber
//                                 min={1}
//                                 max={1000}
//                                 value={maxResults}
//                                 onChange={(value) => setMaxResults(value || 1)}
//                             />
//                         </Form.Item>
//                         <Form.Item>
//                             <Button type="primary" onClick={fetchMails} disabled={loading.length > 0}>
//                                 Buscar E-mails
//                             </Button>
//                         </Form.Item>
//                     </Form>

//                     {/* Overlay de Loading + Gmail List */}
//                     <Spin spinning={loading.length > 0} size="large">
//                         <div style={{ padding: 24, minHeight: 360 }}>
//                             {data?.length > 0 && <GmailLikeList data={data} />}
//                         </div>
//                     </Spin>
//                 </Content>
//                 <Footer style={{ textAlign: 'center' }}>
//                     Gmail Cleaner ©{new Date().getFullYear()} Created by Gabriel Roriz
//                 </Footer>
//             </Layout>
//         </Layout>
//     );
// };

// export default Main;

import React, { useState, useEffect, useRef } from 'react';
import { Layout, Spin, Form, InputNumber, Button } from 'antd';
import SideMenu from './components/SideMenu'; // Novo componente para o menu lateral
import GmailLikeList from './components/GmailLikeList'; // Mantido como estava
import useApi from '../hooks/useApi.hook';
import { getQueryParam, updateURL } from '../utils/urlUtils'; // Funções utilitárias extraídas
import BreadcrumbNav from './components/BreadcrumbNav'; // Novo componente para breadcrumb

const { Content, Footer } = Layout;

const MAX_RESULTS_DEFAULT = 250;

const Main: React.FC = () => {
    const [collapsed, setCollapsed] = useState(false);
    const { loading, getMails } = useApi();
    const hasFetched = useRef(false);

    const [maxResults, setMaxResults] = useState(getQueryParam('max_results') || MAX_RESULTS_DEFAULT);
    const [data, setData] = useState([]);

    const fetchMails = async () => {
        updateURL(maxResults);
        setData(await getMails({ max_results: String(maxResults) }));
    };

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
        fetchMails();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <SideMenu collapsed={collapsed} onCollapse={setCollapsed} />
            <Layout>
                <Content style={{ margin: '0 16px' }}>
                    <BreadcrumbNav />
                    <Form layout="inline" style={{ marginBottom: 16 }}>
                        <Form.Item label="Max Results">
                            <InputNumber
                                min={1}
                                // max={1000}
                                value={maxResults}
                                onChange={(value) => setMaxResults(value || 1)}
                            />
                        </Form.Item>
                        <Form.Item>
                            <Button type="primary" onClick={fetchMails} disabled={loading.length > 0}>
                                Buscar E-mails
                            </Button>
                        </Form.Item>
                    </Form>
                    <Spin spinning={loading.length > 0} size="large">
                        <div style={{ padding: 24, minHeight: 360 }}>
                            {data?.length > 0 && <GmailLikeList data={data} />}
                        </div>
                    </Spin>
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Gmail Cleaner ©{new Date().getFullYear()} Created by Gabriel Roriz
                </Footer>
            </Layout>
        </Layout>
    );
};

export default Main;
