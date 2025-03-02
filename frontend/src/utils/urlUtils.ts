export const getQueryParam = (param: string): number | null => {
    const searchParams = new URLSearchParams(window.location.search);
    const value = searchParams.get(param);
    return value ? parseInt(value, 10) : null;
};

export const updateURL = (newMaxResults: number) => {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set('max_results', newMaxResults.toString());
    const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
    window.history.replaceState(null, '', newUrl);
};