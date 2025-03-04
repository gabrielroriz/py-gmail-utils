import { useEffect, useState, useMemo } from "react";
import { Table, Tag, Button, Modal } from "antd";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { getEmailQuantityBySender, getEmailQuantityByDate, extractUnsubscribeValidLink, formatEmailBody } from "../../utils/gmailUtils";
import { Email, EmailList } from "../Main.types";

function GmailLikeList({ data = [] }: { data: EmailList }) {
    const [emails, setEmails] = useState<EmailList>([]);
    const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);

    useEffect(() => {
        setEmails(data);
    }, [data]);

    const domainData = useMemo(() => getEmailQuantityBySender(emails).slice(0, emails.length < 50 ? 10 : 20), [emails]);
    const dateData = useMemo(() => getEmailQuantityByDate(emails), [emails]);

    const barConfigDomain = {
        chart: { type: 'column' },
        title: { text: 'Quantidade de E-mails por Domínio' },
        xAxis: {
            categories: domainData.map(item => item.domain),
            title: { text: 'Domínio' },
            labels: { rotation: -45 }
        },
        yAxis: { min: 0, title: { text: 'Quantidade de e-mails' } },
        legend: { enabled: false },
        tooltip: { pointFormat: '<b>{point.y}</b> e-mails' },
        series: [{ name: 'E-mails', data: domainData.map(item => item.count), colorByPoint: true }]
    };

    const barConfigData = {
        chart: { type: 'column' },
        title: { text: 'Quantidade de E-mails por Data' },
        xAxis: {
            categories: dateData.map(item => new Date(item.date).toLocaleDateString("pt-BR", { year: 'numeric', month: 'long', day: 'numeric' })),
            title: { text: 'Data' },
            labels: { rotation: -45 }
        },
        yAxis: { min: 0, title: { text: 'Quantidade de e-mails' } },
        legend: { enabled: false },
        tooltip: { pointFormat: '<b>{point.y}</b> e-mails' },
        series: [{ name: 'E-mails', data: dateData.map(item => item.count), colorByPoint: true }]
    };

    const columns = [
        { title: "Remetente", dataIndex: "sender", key: "sender" },
        { title: "Assunto", dataIndex: "subject", key: "subject" },
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
                <>{tags && tags.split(",").map(tag => <Tag key={tag}>{tag.toUpperCase()}</Tag>)}</>
            )
        },
        {
            title: "Descadastro ",
            dataIndex: "unsubscribe_link",
            key: "unsubscribe_link",
            render: (_: string, record: Email) => {
                if (!record.has_unsubscribe) return "N/A";
                const validLink = extractUnsubscribeValidLink(record.unsubscribe_link);
                if (!validLink) return "Mailto Only";

                return <Button type="primary" onClick={() => window.open(validLink, "_blank")}>
                    Cancelar Inscrição
                </Button>;
            }
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
                onRow={(record) => ({
                    onClick: () => setSelectedEmail(record),
                })}
            />
            {data.length > 0 ? (
                <>
                    <HighchartsReact highcharts={Highcharts} options={barConfigDomain} />
                    <HighchartsReact highcharts={Highcharts} options={barConfigData} />
                </>
            ) : (
                <p>Nenhum dado disponível para o gráfico.</p>
            )}

            <Modal
                title="Detalhes do E-mail"
                open={!!selectedEmail}
                onCancel={() => setSelectedEmail(null)}
                footer={null}
                width={1000}
                style={{ overflow: "hidden" }}
            >
                {selectedEmail && (
                    <div>
                        {selectedEmail.has_unsubscribe && extractUnsubscribeValidLink(selectedEmail?.unsubscribe_link) && selectedEmail.unsubscribe_link && (
                            <Button
                                type="primary"
                                onClick={() => selectedEmail?.unsubscribe_link && window.open(extractUnsubscribeValidLink(selectedEmail?.unsubscribe_link), "_blank")}>
                                Cancelar Inscrição
                            </Button>
                        )}
                        <p><strong>Remetente:</strong> {selectedEmail.sender}</p>
                        <p><strong>Assunto:</strong> {selectedEmail.subject}</p>
                        <p><strong>Data:</strong> {new Date(selectedEmail.date).toLocaleDateString("pt-BR", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
                        <p><strong>Labels:</strong> {selectedEmail.label}</p>
                        <p><strong>Snippet:</strong> {selectedEmail.snippet}</p>
                        <p><strong>Corpo:</strong></p>
                        <p>{formatEmailBody(selectedEmail.body)}</p>
                    </div>
                )}
            </Modal>
        </div>
    );
}

export default GmailLikeList;
