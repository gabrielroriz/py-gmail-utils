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
        setData(await getMails({ max_results: String(maxResults), csv_persist: "true" }));
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
