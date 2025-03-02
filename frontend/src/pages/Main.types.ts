export type Email = {
    id: string;
    subject: string;
    sender: string;
    recipients: string;
    body: string;
    snippet: string;
    has_attachments: boolean;
    date: string;
    star: boolean;
    label: string;
};

export type EmailList = Email[];
