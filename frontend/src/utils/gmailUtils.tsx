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

export function getEmailFromSender(sender: string) {
    const match = sender.match(/<([^>]+)>/);
    let emailAddress = "";

    if (match && match[1]) {
        emailAddress = match[1];
    } else {
        emailAddress = sender;
    }

    return emailAddress;  // Retorna o email completo
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

export function getEmailQuantityBySender(emails: EmailList) {
    const counts: Record<string, number> = {};

    emails.forEach((email) => {
        const domain = getEmailFromSender(email.sender);
        counts[domain] = (counts[domain] || 0) + 1;
    });

    return Object.entries(counts).map(([domain, count]) => ({
        domain,
        count,
    })).sort((a, b) => b.count - a.count);
}


export function getEmailQuantityByDate(emails: EmailList) {
    const counts: Record<string, number> = {};

    emails.forEach((email) => {
        const dateObj = new Date(email.date);

        if (isNaN(dateObj.getTime())) {
            console.warn(`Invalid date detected: "${email.date}" - Skipping this email.`);
            return; // Skip invalid dates
        }

        const date = dateObj.toISOString().split("T")[0]; // Extract YYYY-MM-DD
        counts[date] = (counts[date] || 0) + 1;
    });

    return Object.entries(counts)
        .map(([date, count]) => ({ date, count }))
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()); // Sort by date (descending)
}

export function extractUnsubscribeValidLink(unsubscribe_link: string | null) {
    if (!unsubscribe_link) return null;

    const matches = unsubscribe_link.match(/<([^<>]+)>/g); // Captura tudo dentro de <>
    if (!matches) return null; // Retorna null se nenhum link for encontrado

    for (const match of matches) {
        const link = match.slice(1, -1); // Remove os <>
        if (link.startsWith("http://") || link.startsWith("https://")) {
            return link; // Retorna o primeiro link HTTP/HTTPS encontrado
        }
    }

    return null; // Retorna null se nenhum link válido for encontrado
}

export const formatEmailBody = (body: string) => {
    if (!body) return "";

    // Expressão regular para detectar links no texto
    const linkRegex = /\bhttps?:\/\/[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|\/))/gi;

    return body.split("\n").map((line, index) => {
        // Converte links em elementos clicáveis
        const formattedLine = line.replace(linkRegex, (url) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);

        return <p key={index} dangerouslySetInnerHTML={{ __html: formattedLine }} />;
    });
};