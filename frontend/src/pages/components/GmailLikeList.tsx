import { useEffect, useState, useMemo } from "react";

// Components
import { Table, Tag } from "antd";
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

// Utils
import { getEmailQuantityByDomain } from "../../utils/gmailUtils";

// Types
import { EmailList } from "../Main.types";


function GmailLikeList({ data = [] }: { data: EmailList }) {
    const [emails, setEmails] = useState<EmailList>([]);

    useEffect(() => {
        setEmails(data);
    }, [data]);

    const domainData = useMemo(() => getEmailQuantityByDomain(emails), [emails]);


    const barConfig = {
        chart: {
            type: 'column' // Muda de 'bar' (horizontal) para 'column' (vertical)
        },
        title: {
            text: 'Quantidade de E-mails por Domínio'
        },
        xAxis: {
            categories: domainData.map(item => item.domain), // Domínios ordenados
            title: {
                text: 'Domínio'
            },
            labels: {
                rotation: -45 // Rotaciona os rótulos para melhor leitura
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Quantidade de e-mails'
            }
        },
        legend: {
            enabled: false // Oculta a legenda, já que cada barra representa um domínio
        },
        tooltip: {
            pointFormat: '<b>{point.y}</b> e-mails'
        },
        series: [{
            name: 'E-mails',
            data: domainData.map(item => item.count), // Dados ordenados
            colorByPoint: true // Mantém cores diferentes para cada barra
        }]
    };



    // Defina as colunas que serão exibidas
    const columns = [
        {
            title: "Remetente",
            dataIndex: "sender",
            key: "sender",
        },
        {
            title: "Assunto",
            dataIndex: "subject",
            key: "subject",
        },
        {
            title: "Data",
            dataIndex: "date",
            key: "date",
            render: (date: string) => new Date(date).toLocaleDateString("pt-BR", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
        },
        {
            title: "Labels",
            dataIndex: "label",
            key: "label",
            render: (tags: string) => (
                <>
                    {tags && tags.split(",").map((tag: string) => {
                        return (
                            <Tag key={tag} style={{}}>
                                {tag.toUpperCase()}
                            </Tag>
                        );
                    })}
                </>
            ),
        }
    ];

    return (
        <div style={{ padding: 24 }}>
            <h1 style={{ marginBottom: 16 }}>Mail List</h1>
            <Table
                columns={columns}
                dataSource={emails}
                rowKey="id"
                pagination={{ pageSize: 20 }}
            />

            {/* Gráfico de domínios */}
            <h2 style={{ marginBottom: 16 }}>Quantidade de E-mails por Domínio</h2>
            {data.length > 0 ? (
                <>
                    <h1>{data.length}</h1>
                    <HighchartsReact highcharts={Highcharts} options={barConfig} />
                </>
            ) : (
                <p>Nenhum dado disponível para o gráfico.</p>
            )}
        </div>
    );
}

export default GmailLikeList;
