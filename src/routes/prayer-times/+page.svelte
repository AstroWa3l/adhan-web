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
    const fetchInterval = 10000; // 10 seconds
    let audioEnabled = false;
    let darkMode = false;
    let lastPlayedPrayer: string | null = null;
    let isAdhanPlaying = false;

    // New variables for user input
    let city = '';
    let country = '';
    let selectedMethod = 'ISNA'; // Default method
    let methods = ['MWL', 'ISNA', 'Egypt', 'Makkah', 'Karachi', 'Tehran', 'Jafari'];
    let loading = false;
    let errorMessage = '';

    async function fetchPrayerTimesByLocation() {
        loading = true;
        errorMessage = '';

        try {
            if (!city || !country) {
                errorMessage = 'City and Country are required to fetch prayer times.';
                return;
            }

            const response = await fetch(
                `http://127.0.0.1:8000/prayer-times?city=${city}&country=${country}&method=${selectedMethod}`
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch prayer times');
            }

            const data = await response.json();
            prayerTimes = data;

        } catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message || 'An error occurred.';
            } else {
                errorMessage = 'An error occurred.';
            }
            console.error('Failed to fetch prayer times:', error);
        } finally {
            loading = false;
        }
    }

    function toggleDarkMode() {
        darkMode = !darkMode;
        document.body.classList.toggle('dark-mode', darkMode);
    }

    function checkPrayerTime() {
        const now = new Date();
        const currentTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"

        console.log('Prayer Times:', prayerTimes);

        for (const p of ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']) {
            const prayerTime = prayerTimes[p as keyof PrayerTimes];
            console.log(`Checking ${p}:`, prayerTime);

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
        interval = setInterval(() => {
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
    /* Add custom styles for inputs and dropdown */
    .location-form {
        margin: 1rem 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }

    .location-form input,
    .location-form select {
        padding: 0.8rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        width: 80%;
    }

    .error-message {
        color: red;
        font-size: 1rem;
        margin: 0.5rem 0;
    }

    .loading {
        font-size: 1.2rem;
        color: #00FF7F;
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

    <div class="location-form">
        <input
            type="text"
            placeholder="Enter city"
            bind:value={city}
        />
        <input
            type="text"
            placeholder="Enter country"
            bind:value={country}
        />
        <div style="display: flex; align-items: center; gap: 0.5rem; width: 80%;">
            <label for="method-select">Select method:</label>
            <select id="method-select" bind:value={selectedMethod}>
                {#each methods as method}
                    <option value={method}>{method}</option>
                {/each}
            </select>
        </div>
        <button on:click={fetchPrayerTimesByLocation}>
            {loading ? 'Fetching...' : 'Get Prayer Times'}
        </button>
        {#if errorMessage}
            <p class="error-message">{errorMessage}</p>
        {/if}
    </div>

    {#if loading}
        <p class="loading">Loading prayer times...</p>
    {/if}

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
