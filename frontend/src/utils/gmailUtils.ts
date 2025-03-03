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
