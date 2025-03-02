import { useCallback, useState } from "react";

const baseUrl = "http://localhost:5000";

export default () => {

    const [loading, setLoading] = useState<string[]>([]);

    function objectToUrlParams(obj = {}) {
        const params = Object.keys(obj)
            .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]))
            .join('&');

        return params ? '?' + params : '';
    }

    const addLoading = (id: string) => {
        setLoading(current => (current.includes(id) ? current : [...current, id]));
    };

    const removeLoading = (id: string) => {
        setLoading(current => current.filter((item) => item !== id))
    }

    const getMails = useCallback(async (params: Record<string, string> = {}) => {
        const id = "GET_MAILS";

        try {
            addLoading(id);
            const response = await fetch(`${baseUrl}/${objectToUrlParams(params)}`);
            return response.json();
        } finally {
            removeLoading(id);
        }
    }, []);


    return { loading, getMails }
}