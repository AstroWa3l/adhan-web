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
    const fetchInterval = 10000; // 10 seconds
    let audioEnabled = false; // Track if audio playback is enabled
    let darkMode = false; // Track dark mode state
    let lastPlayedPrayer: string | null = null; // Track the last prayer time for which Adhan was played

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
                if (lastPlayedPrayer !== p) {
                    console.log(`Current time matches ${p}! Playing Adhan.`);
                    playAdhan();
                    lastPlayedPrayer = p; // Mark this prayer as played
                } else {
                    console.log(`Adhan for ${p} has already been played.`);
                }
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

    function resetDailyPrayerState() {
        lastPlayedPrayer = null;
        console.log('Resetting last played prayer for the new day.');
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
    });

    onDestroy(() => {
        clearInterval(interval);
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

/* Table styles */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    margin: 1rem 0;
    color: #333;
    background: rgba(255, 255, 255, 0.9);
    transition: background 0.3s ease, color 0.3s ease;
}

table.dark-mode {
    background: rgba(30, 30, 30, 0.9);
    color: #e0e0e0;
}

table tr:hover {
    background-color: rgba(0, 255, 127, 0.2);
}

th, td {
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(200, 200, 200, 0.5);
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
                <th class="{darkMode ? 'dark-mode' : ''}">Date</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Fajr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Dhuhr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Asr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Maghrib</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Isha</th>
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

    {#if adhanAudio && !adhanAudio.paused}
        <div class="adhan-playing">🎵 Adhan is playing...</div>
    {/if}

    <button on:click={stopAdhan}>Silence Adhan</button>
    <audio bind:this={adhanAudio} src="/adhan.mp3" preload="auto"></audio>
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
    
    let prayerTimes: Partial<PrayerTimes> = {}; // Store the prayer times
    let adhanAudio: HTMLAudioElement;
    let interval: number;
    const fetchInterval = 10000; // 10 seconds
    let audioEnabled = false; // Track if audio playback is enabled
    let darkMode = false; // Track dark mode state
    let lastPlayedPrayer: string | null = null; // Track the last prayer time for which Adhan was played

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
                // Check if this prayer has already been played for this minute
                if (lastPlayedPrayer !== `${p}-${currentTimeStr}`) {
                    console.log(`Current time matches ${p}! Playing Adhan.`);
                    playAdhan();
                    lastPlayedPrayer = `${p}-${currentTimeStr}`; // Update with prayer and time
                } else {
                    console.log(`Adhan for ${p} at ${currentTimeStr} has already been played.`);
                }
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

    function resetDailyPrayerState() {
        lastPlayedPrayer = null;
        console.log('Resetting last played prayer for the new day.');
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
    });

    onDestroy(() => {
        clearInterval(interval);
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

/* Table styles */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    margin: 1rem 0;
    color: #333;
    background: rgba(255, 255, 255, 0.9);
    transition: background 0.3s ease, color 0.3s ease;
}

table.dark-mode {
    background: rgba(30, 30, 30, 0.9);
    color: #e0e0e0;
}

table tr:hover {
    background-color: rgba(0, 255, 127, 0.2);
}

th, td {
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(200, 200, 200, 0.5);
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
                <th class="{darkMode ? 'dark-mode' : ''}">Date</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Fajr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Dhuhr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Asr</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Maghrib</th>
                <th class="{darkMode ? 'dark-mode' : ''}">Isha</th>
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

    {#if adhanAudio && !adhanAudio.paused}
        <div class="adhan-playing">🎵 Adhan is playing...</div>
    {/if}

    <button on:click={stopAdhan}>Silence Adhan</button>
    <audio bind:this={adhanAudio} src="/adhan.mp3" preload="auto"></audio>
</div>
