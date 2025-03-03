import { useEffect, useState, useMemo } from "react";

// Components
import { Table, Tag } from "antd";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

// Utils
import { getEmailQuantityByDomain, getEmailQuantityByDate } from "../../utils/gmailUtils";

// Types
import { EmailList } from "../Main.types";


function GmailLikeList({ data = [] }: { data: EmailList }) {
    const [emails, setEmails] = useState<EmailList>([]);

    useEffect(() => {
        setEmails(data);
    }, [data]);

    const domainData = useMemo(() => getEmailQuantityByDomain(emails).slice(0, emails.length < 50 ? 10 : 20), [emails]);


    const dateData = useMemo(() => getEmailQuantityByDate(emails), [emails]);

    const barConfigDomain = {
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

    const barConfigData = {
        chart: {
            type: 'column' // Muda de 'bar' (horizontal) para 'column' (vertical)
        },
        title: {
            text: 'Quantidade de E-mails por Data'
        },
        xAxis: {
            categories: dateData.map(item => {
                console.log(item.date);
                return new Date(item.date).toLocaleDateString("pt-BR", { year: 'numeric', month: 'long', day: 'numeric' })
            }),// Domínios ordenados
            title: {
                text: 'Data'
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
            data: dateData.map(item => item.count), // Dados ordenados
            colorByPoint: true // Mantém cores diferentes para cada barra
        }]
    };

    const heatmapConfig = {
        chart: { type: "heatmap" },
        title: { text: "E-mails por Dia do Mês" },
        xAxis: {
            categories: dateData.map(item => item.date),
            title: { text: "Dia do Mês" }
        },
        yAxis: {
            title: { text: "E-mails" },
            labels: { enabled: false }
        },
        colorAxis: {
            min: 0,
            max: Math.max(...dateData.map(item => item.count)),
            stops: [[0, "#ffffff"], [0.5, "#ffbf00"], [1, "#ff0000"]]
        },
        series: [{
            name: "E-mails",
            data: dateData.map((item, index) => [index, 0, item.count]),
            dataLabels: { enabled: true, color: "#000" }
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
            <h1 style={{ marginBottom: 16 }}>Lista de E-mails</h1>
            <Table
                columns={columns}
                dataSource={emails}
                rowKey="id"
                pagination={{ pageSize: 20 }}
            />


            {data.length > 0 ? (
                <>
                    {/* Gráfico de domínios */}
                    <HighchartsReact highcharts={Highcharts} options={barConfigDomain} />
                    {/* Gráfico de datas */}
                    <HighchartsReact highcharts={Highcharts} options={barConfigData} />
                    {/* <HighchartsReact highcharts={Highcharts} options={heatmapConfig} /> */}
                </>
            ) : (
                <p>Nenhum dado disponível para o gráfico.</p>
            )}
        </div>
    );
}

export default GmailLikeList;
