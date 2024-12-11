<!-- <script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    interface PrayerTimes {
        date: string;
        fajr: string;
        dhuhr: string;
        asr: string;
        maghrib: string;
        isha: string;
    }
    
    let prayerTimes: Partial<PrayerTimes> = {}; // Store the prayer times
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 60000; // 60 seconds

    // Fetch prayer times from the backend
    async function fetchPrayerTimes() {
        try {
            const res = await fetch('http://127.0.0.1:8000/prayer-times');
            const data = await res.json();
            prayerTimes = data;
            console.log('Updated prayerTimes:', prayerTimes); // Log updated times
        } catch (error) {
            console.error('Failed to fetch prayer times:', error);
        }
    }

    // Check every minute if the current time matches a prayer time
    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        console.log('Current Time:', currentTimeStr);
        console.log('Prayer Times:', prayerTimes);

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            console.log(`Checking ${p}:`, prayerTime);

            if (prayerTime && currentTimeStr === prayerTime) {
                console.log(`Current time matches ${p}!`);
                playAdhan();
            }
        }
    }

    // Play the Adhan
    function playAdhan() {
        if (adhanAudio) {
            console.log('Playing Adhan...');
            adhanAudio.currentTime = 0;
            adhanAudio.play().catch((err) => console.error('Adhan playback failed:', err));
        } else {
            console.error('Adhan audio element not found.');
        }
    }

    // Stop the Adhan
    function stopAdhan() {
        if (adhanAudio && !adhanAudio.paused) {
            adhanAudio.pause();
            adhanAudio.currentTime = 0;
        }
    }

    onMount(() => {
        // Fetch prayer times initially
        fetchPrayerTimes();

        // Re-fetch prayer times every 60 seconds
        interval = setInterval(() => {
            fetchPrayerTimes();
            checkPrayerTime(); // Check after updating times
        }, fetchInterval);
    });

    onDestroy(() => {
        clearInterval(interval); // Clear interval when the component is destroyed
    });
</script>

<style>
table {
    border-collapse: collapse;
    margin: 0 auto;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

button {
    margin: 20px;
    display: block;
}
</style>

<h1 style="text-align: center;">Today's Prayer Times</h1>
<table>
    <thead>
        <tr>
            <th>Date</th>
            <th>Fajr</th>
            <th>Dhuhr</th>
            <th>Asr</th>
            <th>Maghrib</th>
            <th>Isha</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{prayerTimes.date || 'N/A'}</td>
            <td>{prayerTimes.fajr || 'N/A'}</td>
            <td>{prayerTimes.dhuhr || 'N/A'}</td>
            <td>{prayerTimes.asr || 'N/A'}</td>
            <td>{prayerTimes.maghrib || 'N/A'}</td>
            <td>{prayerTimes.isha || 'N/A'}</td>
        </tr>
    </tbody>
</table>

<audio bind:this={adhanAudio} src="/adhan.mp3" preload="auto"></audio>

<button on:click={stopAdhan}>Silence Adhan</button> -->


<!-- <script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    interface PrayerTimes {
        date: string;
        fajr: string;
        dhuhr: string;
        asr: string;
        maghrib: string;
        isha: string;
    }
    
    let prayerTimes: Partial<PrayerTimes> = {}; // Store the prayer times
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 60000; // 60 seconds
    let audioEnabled = false; // Track if audio playback is enabled

    // Fetch prayer times from the backend
    async function fetchPrayerTimes() {
        try {
            const res = await fetch('http://127.0.0.1:8000/prayer-times');
            const data = await res.json();
            prayerTimes = data;
            console.log('Updated prayerTimes:', prayerTimes); // Log updated times
        } catch (error) {
            console.error('Failed to fetch prayer times:', error);
        }
    }

    // Check every minute if the current time matches a prayer time
    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        console.log('Current Time:', currentTimeStr);
        console.log('Prayer Times:', prayerTimes);

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            console.log(`Checking ${p}:`, prayerTime);

            if (prayerTime && currentTimeStr === prayerTime) {
                console.log(`Current time matches ${p}!`);
                playAdhan();
            }
        }
    }

    // Enable audio by playing and pausing the Adhan
    function enableAudio() {
        if (adhanAudio) {
            adhanAudio.play().then(() => {
                adhanAudio.pause(); // Pause immediately after playing to "unlock" audio
                audioEnabled = true;
                console.log('Audio permission granted.');
            }).catch((err) => console.error('Failed to enable audio:', err));
        }
    }

    // Play the Adhan
    function playAdhan() {
        if (audioEnabled && adhanAudio) {
            console.log('Playing Adhan...');
            adhanAudio.currentTime = 0;
            adhanAudio.play().catch((err) => console.error('Adhan playback failed:', err));
        } else {
            console.warn('Audio is not enabled yet.');
        }
    }

    // Stop the Adhan
    function stopAdhan() {
        if (adhanAudio && !adhanAudio.paused) {
            adhanAudio.pause();
            adhanAudio.currentTime = 0;
        }
    }

    onMount(() => {
        // Fetch prayer times initially
        fetchPrayerTimes();

        // Re-fetch prayer times every 60 seconds
        interval = setInterval(() => {
            fetchPrayerTimes();
            checkPrayerTime(); // Check after updating times
        }, fetchInterval);
    });

    onDestroy(() => {
        clearInterval(interval); // Clear interval when the component is destroyed
    });
</script>

<style>
table {
    border-collapse: collapse;
    margin: 0 auto;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

button {
    margin: 20px;
    display: block;
}
</style>

<h1 style="text-align: center;">Today's Prayer Times</h1>
<table>
    <thead>
        <tr>
            <th>Date</th>
            <th>Fajr</th>
            <th>Dhuhr</th>
            <th>Asr</th>
            <th>Maghrib</th>
            <th>Isha</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{prayerTimes.date || 'N/A'}</td>
            <td>{prayerTimes.fajr || 'N/A'}</td>
            <td>{prayerTimes.dhuhr || 'N/A'}</td>
            <td>{prayerTimes.asr || 'N/A'}</td>
            <td>{prayerTimes.maghrib || 'N/A'}</td>
            <td>{prayerTimes.isha || 'N/A'}</td>
        </tr>
    </tbody>
</table>

{#if !audioEnabled}
    <div style="text-align: center; margin: 20px;">
        <p>Click below to enable audio playback for the Adhan.</p>
        <button on:click={enableAudio}>Enable Audio</button>
    </div>
{/if}

<audio bind:this={adhanAudio} src="/adhan.mp3" preload="auto"></audio>

<button on:click={stopAdhan}>Silence Adhan</button> -->

<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    interface PrayerTimes {
        date: string;
        fajr: string;
        dhuhr: string;
        asr: string;
        maghrib: string;
        isha: string;
    }
    
    let prayerTimes: Partial<PrayerTimes> = {}; // Store the prayer times
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 60000; // 60 seconds
    let audioEnabled = false; // Track if audio playback is enabled

    async function fetchPrayerTimes() {
        try {
            const res = await fetch('http://127.0.0.1:8000/prayer-times');
            const data = await res.json();
            prayerTimes = data;
        } catch (error) {
            console.error('Failed to fetch prayer times:', error);
        }
    }

    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            if (prayerTime && currentTimeStr === prayerTime) {
                playAdhan();
            }
        }
    }

    function enableAudio() {
        if (adhanAudio) {
            adhanAudio.play().then(() => {
                adhanAudio.pause(); // Pause immediately after playing to "unlock" audio
                audioEnabled = true;
                console.log('Audio permission granted.');
            }).catch((err) => console.error('Failed to enable audio:', err));
        }
    }

    function playAdhan() {
        if (audioEnabled && adhanAudio) {
            adhanAudio.currentTime = 0;
            adhanAudio.play().catch((err) => console.error('Adhan playback failed:', err));
        }
    }

    function stopAdhan() {
        if (adhanAudio && !adhanAudio.paused) {
            adhanAudio.pause();
            adhanAudio.currentTime = 0;
        }
    }

    onMount(() => {
        fetchPrayerTimes();
        interval = setInterval(() => {
            fetchPrayerTimes();
            checkPrayerTime();
        }, fetchInterval);
    });

    onDestroy(() => {
        clearInterval(interval);
    });
</script>

<style>
body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(to right, #2193b0, #6dd5ed);
    color: #fff;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Center the container with the table */
.container {
    background: rgba(255, 255, 255, 0.2);
    padding: 2rem;
    border-radius: 12px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 800px;
    width: 90%;
}

/* Table styles */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    color: #333;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    overflow: hidden;
}

th, td {
    padding: 1rem;
    text-align: center;
    border: 1px solid #ddd;
}

th {
    background: #6dd5ed;
    color: #fff;
    font-size: 1.2rem;
}

td {
    font-size: 1rem;
}

/* Buttons */
button {
    background: #2193b0;
    color: #fff;
    border: none;
    padding: 0.8rem 1.2rem;
    margin-top: 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s;
}

button:hover {
    background: #6dd5ed;
}

/* Responsive */
@media (max-width: 600px) {
    th, td {
        font-size: 0.9rem;
        padding: 0.5rem;
    }

    button {
        font-size: 0.9rem;
    }
}
</style>

<div class="container">
    <h1>Today's Prayer Times</h1>
    <p>Stay on top of your prayers with this schedule.</p>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Fajr</th>
                <th>Dhuhr</th>
                <th>Asr</th>
                <th>Maghrib</th>
                <th>Isha</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{prayerTimes.date || 'N/A'}</td>
                <td>{prayerTimes.fajr || 'N/A'}</td>
                <td>{prayerTimes.dhuhr || 'N/A'}</td>
                <td>{prayerTimes.asr || 'N/A'}</td>
                <td>{prayerTimes.maghrib || 'N/A'}</td>
                <td>{prayerTimes.isha || 'N/A'}</td>
            </tr>
        </tbody>
    </table>

    {#if !audioEnabled}
        <div style="margin: 20px;">
            <p>Click below to enable audio playback for the Adhan.</p>
            <button on:click={enableAudio}>Enable Audio</button>
        </div>
    {/if}

    <button on:click={stopAdhan}>Silence Adhan</button>
    <audio bind:this={adhanAudio} src="/adhan.mp3" preload="auto"></audio>
</div>
