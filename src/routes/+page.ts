export async function load({ fetch }) {
    const city = encodeURIComponent('Acton');
    const state = encodeURIComponent('CA');
    const country = encodeURIComponent('United States');
    const method = encodeURIComponent('ISNA');

    const res = await fetch(`http://127.0.0.1:8000/?city=${city}&state=${state}&country=${country}&method=${method}`);
    if (!res.ok) {
        console.error('Failed to fetch prayer times:', res.status, res.statusText);
        return { prayerTimes: {} };
    }

    const data = await res.json();
    return { prayerTimes: data };
}