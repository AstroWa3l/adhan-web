export async function load({ fetch }) {
    const res = await fetch('http://127.0.0.1:8000/prayer-times');
    if (!res.ok) {
        console.error('Failed to fetch prayer times:', res.status, res.statusText);
        return { prayerTimes: {} };
    }

    const data = await res.json();
    return { prayerTimes: data };
}
