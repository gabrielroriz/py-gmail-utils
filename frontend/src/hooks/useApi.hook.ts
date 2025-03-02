import { useCallback } from "react";

const baseUrl = "http://localhost:5000";

export default () => {

    function objectToUrlParams(obj = {}) {
        const params = Object.keys(obj)
            .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]))
            .join('&');

        return params ? '?' + params : '';
    }
    const getMails = useCallback(async (params = {}) => {
        return (await fetch(`${baseUrl}/${objectToUrlParams(params)}`)).json();
    }, []);

    return { getMails }
}