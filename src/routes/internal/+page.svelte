<script lang="ts">
	import People from './components/people.svelte';
	import Rankings from './components/rankings.svelte';
	import Schedule from './components/schedule.svelte';
	import Timer from './components/timer.svelte';
	import Event from './components/event.svelte';
	import Announcements from './components/announcements.svelte';
	import Stream from './components/livestream.svelte';
	import { showRotations } from '$lib/config';
	import { onDestroy, onMount } from 'svelte';

	let scheduleVisible = $state(true)
	let shouldUpdate = $state(false)
	let timeUntilSwitch = 0;
	let hasRankings = false;
	
	const toggle = () => scheduleVisible = !scheduleVisible;

	function tick() {
		timeUntilSwitch -= 1;
		if (timeUntilSwitch <= 0) {
			if (scheduleVisible) {
				if (hasRankings) toggle()
				timeUntilSwitch = 20;
			}
			else {
				toggle()
				timeUntilSwitch = 30;
			}
		}
	}

	async function updateRankings() {
		const res = await fetch("/api/rankings");
		const data = await res.json();
		if (data.length > 0) hasRankings = true;
		else hasRankings = false;
	}

	let tickInterval: NodeJS.Timeout;
	let rankingsInterval: NodeJS.Timeout;
	onMount(async () => {
		timeUntilSwitch = 30;
		tickInterval = setInterval(tick, 1000)
		await updateRankings()
		rankingsInterval = setInterval(updateRankings, 60 * 1000)
	})

	onDestroy(() => {
		clearInterval(tickInterval);
		clearInterval(rankingsInterval);
	}
	)

	function openFullScreen() {
		document.documentElement.requestFullscreen();
	}
</script>

<head>
	<title>The Holy Hen has Acquired Sight</title>
</head>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="main h-screen w-screen overflow-hidden" onclick={openFullScreen}>
	<button style="grid-area: schedule" onclick={toggle}>
		{#if scheduleVisible}
			<Schedule></Schedule>
		{:else}
			<Rankings bind:scheduleVisible = {scheduleVisible}></Rankings>
		{/if}
	</button>
	<div style="grid-area: timer;"><Timer bind:shouldUpdate = { shouldUpdate }></Timer></div>
	<div style="grid-area: event;"><Event bind:shouldUpdate = { shouldUpdate }></Event></div>
	{#if showRotations}
		<div style="grid-area: announcements;"><People></People></div>
	{:else}
		<div style="grid-area: announcements;"><Announcements></Announcements></div>
	{/if}
	<div style="grid-area: big"><Stream></Stream></div>
</div>

<style>
	.main {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		grid-template-rows: repeat(5, 1fr);
		grid-template-areas:
			'big big schedule'
			'big big schedule'
			'big big schedule'
			'announcements event timer'
			'announcements event timer';
		gap: 20px;
	}
</style>
