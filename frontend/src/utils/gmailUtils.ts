import { EmailList } from "../pages/Main.types";

export function getDomainFromSender(sender: string) {
    const match = sender.match(/<([^>]+)>/);
    let emailAddress = "";

    if (match && match[1]) {
        emailAddress = match[1];
    } else {
        emailAddress = sender;
    }

    const atIndex = emailAddress.indexOf("@");
    if (atIndex !== -1) {
        return emailAddress.substring(atIndex);
    }
    return "(domínio desconhecido)";
}

export function getEmailQuantityByDomain(emails: EmailList) {
    const counts: Record<string, number> = {};

    emails.forEach((email) => {
        const domain = getDomainFromSender(email.sender);
        counts[domain] = (counts[domain] || 0) + 1;
    });

    return Object.entries(counts).map(([domain, count]) => ({
        domain,
        count,
    })).sort((a, b) => b.count - a.count);
}