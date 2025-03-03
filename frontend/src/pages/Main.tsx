import React, { useState, useEffect, useRef } from 'react';
import { Layout, Spin, Form, InputNumber, Button, Select } from 'antd';
import { SyncOutlined } from '@ant-design/icons'; // Importa o ícone de recarregar
import SideMenu from './components/SideMenu';
import GmailLikeList from './components/GmailLikeList';
import useApi from '../hooks/useApi.hook';
import { getQueryParam, updateURL } from '../utils/urlUtils';
import BreadcrumbNav from './components/BreadcrumbNav';

const { Content, Footer } = Layout;
const { Option } = Select;

const MAX_RESULTS_DEFAULT = 250;


const Main: React.FC = () => {
    const [collapsed, setCollapsed] = useState(false);
    const { loading, getMails, getCsvDatabases } = useApi();
    const hasFetched = useRef(false);

    const [databases, setDatabases] = useState<string[]>([]);

    // Data
    const [data, setData] = useState([]);

    // Filters
    const [maxResults, setMaxResults] = useState(getQueryParam('max_results') || MAX_RESULTS_DEFAULT);
    const [selectedDatabase, setSelectedDatabase] = useState(getQueryParam('database'));

    const fetchMails = async () => {
        updateURL(maxResults);
        setData(await getMails({
            max_results: String(maxResults),
            csv_persist: "true",
            // database: selectedDatabase // Passa o banco de dados selecionado
        }));
    };


    const fetchCsvDatabases = async () => {
        // updateURL(maxResults);
        const response = await getCsvDatabases();
        setDatabases(response.data);
    };

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
        fetchMails();
        fetchCsvDatabases();
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
                                value={maxResults}
                                onChange={(value) => setMaxResults(value || 1)}
                            />
                        </Form.Item>
                        <Form.Item label="Database">
                            <Select
                                style={{ width: 250 }}
                                value={selectedDatabase}
                                onChange={setSelectedDatabase}
                            >
                                {databases.map(db => (
                                    <Option key={db} value={db}>
                                        {db}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>
                        <Form.Item>
                            <Button
                                icon={<SyncOutlined />}
                                onClick={fetchCsvDatabases}
                                disabled={loading.length > 0}
                                style={{ marginRight: 8 }}
                            >
                                Refresh
                            </Button>
                        </Form.Item>
                        <Form.Item>
                            <Button
                                type="primary"
                                onClick={fetchMails}
                                disabled={loading.length > 0}
                            >
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