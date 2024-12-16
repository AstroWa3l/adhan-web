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
    
    let prayerTimes: Partial<PrayerTimes> = {};
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 10000; // 10 seconds
    let audioEnabled = false;
    let darkMode = false;
    let lastPlayedPrayer: string | null = null;
    let isAdhanPlaying = false; // Track if Adhan is currently playing

    async function fetchPrayerTimes() {
        try {
            const res = await fetch('http://127.0.0.1:8000/prayer-times');
            const data = await res.json();
            prayerTimes = data;
        } catch (error) {
            console.error('Failed to fetch prayer times:', error);
        }
    }

    function toggleDarkMode() {
        darkMode = !darkMode;
        document.body.classList.toggle('dark-mode', darkMode);
    }

    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        console.log('Current Time:', currentTimeStr);
        console.log('Prayer Times:', prayerTimes);

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            console.log(`Checking ${p}:`, prayerTime);

            if (prayerTime && currentTimeStr === prayerTime) {
                if (lastPlayedPrayer !== p) {
                    console.log(`Current time matches ${p}! Playing Adhan.`);
                    playAdhan();
                    lastPlayedPrayer = p;
                } else {
                    console.log(`Adhan for ${p} has already been played.`);
                }
            }
        }
    }

    function enableAudio() {
        if (adhanAudio) {
            adhanAudio.play()
                .then(() => {
                    adhanAudio.pause();
                    audioEnabled = true;
                    console.log('Audio permission granted.');
                })
                .catch((err) => console.error('Failed to enable audio:', err));
        }
    }

    function playAdhan() {
        if (audioEnabled && adhanAudio && !isAdhanPlaying) {
            adhanAudio.currentTime = 0;
            adhanAudio.play()
                .then(() => {
                    isAdhanPlaying = true;
                    console.log('Adhan started playing.');
                })
                .catch((err) => console.error('Adhan playback failed:', err));
        }
    }

    function stopAdhan() {
        if (adhanAudio && !adhanAudio.paused) {
            adhanAudio.pause();
            adhanAudio.currentTime = 0;
            isAdhanPlaying = false;
            console.log('Adhan playback stopped.');
        }
    }

    function resetDailyPrayerState() {
        lastPlayedPrayer = null;
        console.log('Resetting last played prayer for the new day.');
    }

    function handleAdhanEnded() {
        isAdhanPlaying = false;
        console.log('Adhan finished playing.');
    }

    onMount(() => {
        fetchPrayerTimes();
        interval = setInterval(() => {
            fetchPrayerTimes();
            checkPrayerTime();
        }, fetchInterval);

        const midnight = new Date();
        midnight.setHours(24, 0, 0, 0); // Next midnight
        const timeToMidnight = midnight.getTime() - Date.now();

        setTimeout(() => {
            resetDailyPrayerState();
            setInterval(resetDailyPrayerState, 24 * 60 * 60 * 1000); // Reset daily
        }, timeToMidnight);

        if (adhanAudio) {
            adhanAudio.addEventListener('ended', handleAdhanEnded);
        }
    });

    onDestroy(() => {
        clearInterval(interval);
        if (adhanAudio) {
            adhanAudio.removeEventListener('ended', handleAdhanEnded);
        }
    });
</script>

<style>
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

    .container.dark-mode {
        background: rgba(0, 0, 0, 0.5);
    }

    /* Table styles */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        color: #333;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        overflow: hidden;
        transition: background 0.3s ease, color 0.3s ease;
    }

    table.dark-mode {
        background: rgba(30, 30, 30, 0.9);
        color: #e0e0e0;
    }

    th, td {
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(200, 200, 200, 0.5);
    }

    th {
        background: #00FF7F;
        color: #000000;
        font-size: 1.2rem;
    }

    td {
        font-size: 1rem;
    }

    /* Buttons */
    button {
        background: linear-gradient(to right, #00FF7F, #6dd5ed);
        color: #000000;
        border: none;
        padding: 0.8rem 1.5rem;
        margin-top: 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        transition: transform 0.2s, background 0.3s;
    }

    button:hover {
        transform: scale(1.1);
        background: linear-gradient(to right, #6dd5ed, #00FF7F);
    }

    /* Toggle Button */
    .toggle-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.5rem;
        color: inherit;
        position: absolute;
        top: 20px;
        right: 20px;
        transition: transform 0.3s ease;
    }

    .toggle-button:hover {
        transform: scale(1.2);
    }

    /* Adhan playing feedback */
    .adhan-playing {
        font-size: 1.2rem;
        color: #00FF7F;
        margin: 20px 0;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    /* Responsive */
    @media (max-width: 600px) {
        .container {
            padding: 1rem;
        }

        th, td {
            font-size: 0.9rem;
            padding: 0.5rem;
        }

        button {
            font-size: 0.9rem;
        }
    }
</style>

<div class="container {darkMode ? 'dark-mode' : ''}">
    <button class="toggle-button" on:click={toggleDarkMode}>
        {#if darkMode}
            <i class="fas fa-sun"></i>
        {:else}
            <i class="fas fa-moon"></i>
        {/if}
    </button>
    <h1>Today's Prayer Times</h1>
    <p>Stay on top of your prayers with this schedule.</p>
    <table class="{darkMode ? 'dark-mode' : ''}">
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
        <div style="margin: 20px; text-align: center; font-size: 1.2rem;">
            <p>🔊 Click below to enable audio playback for the Adhan.</p>
            <button on:click={enableAudio}>Enable Audio</button>
        </div>
    {/if}

    {#if isAdhanPlaying}
        <div class="adhan-playing">🎵 Adhan is playing...</div>
    {/if}

    <button on:click={stopAdhan}>Silence Adhan</button>
    <audio
        bind:this={adhanAudio}
        src="/adhan.mp3"
        preload="auto"
        on:ended={handleAdhanEnded}
    ></audio>
</div> -->

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

    let prayerTimes: Partial<PrayerTimes> = {};
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 60000; // 60 seconds
    let audioEnabled = false;
    let darkMode = false;
    let lastPlayedPrayer: string | null = null;
    let isAdhanPlaying = false;

    // Variables for user input
    let latitude: string = '';
    let longitude: string = '';

    async function fetchPrayerTimes() {
        try {
            if (!latitude || !longitude) {
                console.error('Latitude and longitude are required.');
                return;
            }

            const res = await fetch(`http://127.0.0.1:8000/prayer-times?latitude=${latitude}&longitude=${longitude}`);
            if (!res.ok) {
                throw new Error('Failed to fetch prayer times.');
            }
            const data = await res.json();
            prayerTimes = data;
        } catch (error) {
            console.error('Failed to fetch prayer times:', error);
        }
    }

    function toggleDarkMode() {
        darkMode = !darkMode;
        document.body.classList.toggle('dark-mode', darkMode);
    }

    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            if (prayerTime && currentTimeStr === prayerTime) {
                if (lastPlayedPrayer !== p) {
                    playAdhan();
                    lastPlayedPrayer = p;
                }
            }
        }
    }

    function enableAudio() {
        if (adhanAudio) {
            adhanAudio.play()
                .then(() => {
                    adhanAudio.pause();
                    audioEnabled = true;
                })
                .catch((err) => console.error('Failed to enable audio:', err));
        }
    }

    function playAdhan() {
        if (audioEnabled && adhanAudio && !isAdhanPlaying) {
            adhanAudio.currentTime = 0;
            adhanAudio.play()
                .then(() => {
                    isAdhanPlaying = true;
                })
                .catch((err) => console.error('Adhan playback failed:', err));
        }
    }

    function stopAdhan() {
        if (adhanAudio && !adhanAudio.paused) {
            adhanAudio.pause();
            adhanAudio.currentTime = 0;
            isAdhanPlaying = false;
        }
    }

    function resetDailyPrayerState() {
        lastPlayedPrayer = null;
    }

    function handleAdhanEnded() {
        isAdhanPlaying = false;
    }

    onMount(() => {
        // Optionally get user's current location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    latitude = position.coords.latitude.toString();
                    longitude = position.coords.longitude.toString();
                    fetchPrayerTimes();
                },
                (error) => {
                    console.error('Error getting location:', error);
                    // Prompt user to enter latitude and longitude
                }
            );
        } else {
            console.error('Geolocation is not supported by this browser.');
            // Prompt user to enter latitude and longitude
        }

        interval = setInterval(() => {
            fetchPrayerTimes();
            checkPrayerTime();
        }, fetchInterval);

        const midnight = new Date();
        midnight.setHours(24, 0, 0, 0); // Next midnight
        const timeToMidnight = midnight.getTime() - Date.now();

        setTimeout(() => {
            resetDailyPrayerState();
            setInterval(resetDailyPrayerState, 24 * 60 * 60 * 1000); // Reset daily
        }, timeToMidnight);

        if (adhanAudio) {
            adhanAudio.addEventListener('ended', handleAdhanEnded);
        }
    });

    onDestroy(() => {
        clearInterval(interval);
        if (adhanAudio) {
            adhanAudio.removeEventListener('ended', handleAdhanEnded);
        }
    });
</script>

<style>
    /* Container styles */
    .container {
        background: rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 12px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        max-width: 800px;
        width: 90%;
        margin: 0 auto;
    }

    .container.dark-mode {
        background: rgba(0, 0, 0, 0.5);
    }

    /* Table styles */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        color: #333;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        overflow: hidden;
        transition: background 0.3s ease, color 0.3s ease;
    }

    table.dark-mode {
        background: rgba(30, 30, 30, 0.9);
        color: #e0e0e0;
    }

    th, td {
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(200, 200, 200, 0.5);
    }

    th {
        background: #00FF7F;
        color: #000000;
        font-size: 1.2rem;
    }

    td {
        font-size: 1rem;
    }

    /* Buttons */
    button {
        background: linear-gradient(to right, #00FF7F, #6dd5ed);
        color: #000;
        border: none;
        padding: 0.8rem 1.5rem;
        margin-top: 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        transition: transform 0.2s, background 0.3s;
    }

    button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #6dd5ed, #00FF7F);
    }

    /* Toggle Button */
    .toggle-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.5rem;
        color: inherit;
        position: absolute;
        top: 20px;
        right: 20px;
        transition: transform 0.3s ease;
    }

    .toggle-button:hover {
        transform: scale(1.2);
    }

    /* Location Inputs */
    .location-inputs {
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .location-inputs label {
        margin: 0.5rem 0;
        font-size: 1rem;
        color: inherit;
    }

    .location-inputs input {
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #ccc;
        margin-top: 0.3rem;
        width: 200px;
    }

    .location-inputs button {
        background: linear-gradient(to right, #00FF7F, #6dd5ed);
        color: #000;
        border: none;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 0.5rem;
        transition: transform 0.2s, background 0.3s;
    }

    .location-inputs button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #6dd5ed, #00FF7F);
    }

    /* Adhan playing feedback */
    .adhan-playing {
        font-size: 1.2rem;
        color: #00FF7F;
        margin: 20px 0;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>

<div class="container {darkMode ? 'dark-mode' : ''}">
    <button class="toggle-button" on:click={toggleDarkMode}>
        {#if darkMode}
            <i class="fas fa-sun"></i>
        {:else}
            <i class="fas fa-moon"></i>
        {/if}
    </button>
    <h1>Today's Prayer Times</h1>

    <!-- Location Inputs -->
    <div class="location-inputs">
        <label>
            Latitude:
            <input type="number" bind:value={latitude} placeholder="Enter latitude" step="any">
        </label>
        <label>
            Longitude:
            <input type="number" bind:value={longitude} placeholder="Enter longitude" step="any">
        </label>
        <button on:click={fetchPrayerTimes}>Get Prayer Times</button>
    </div>

    <!-- Prayer Times Table -->
    <table class="{darkMode ? 'dark-mode' : ''}">
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
        <div style="margin: 20px; text-align: center; font-size: 1.2rem;">
            <p>🔊 Click below to enable audio playback for the Adhan.</p>
            <button on:click={enableAudio}>Enable Audio</button>
        </div>
    {/if}

    {#if isAdhanPlaying}
        <div class="adhan-playing">🎵 Adhan is playing...</div>
    {/if}

    <button on:click={stopAdhan}>Silence Adhan</button>
    <audio
        bind:this={adhanAudio}
        src="/adhan.mp3"
        preload="auto"
        on:ended={handleAdhanEnded}
    ></audio>
</div>