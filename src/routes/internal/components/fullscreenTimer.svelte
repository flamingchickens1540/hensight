<script lang="ts">
	import { beforeNavigate } from '$app/navigation';
import type { formattedTimer } from '$lib/types';
	import { onDestroy, onMount } from 'svelte';
	import { source } from 'sveltekit-sse';
	let { fullscreen = $bindable() } = $props();

	const msToTime = (ms: number) => new Date(ms).toTimeString().split(' ')[0];

	function msToRelative(ms: number): string {
		let seconds = ms / 1000;
		let days = Math.floor(seconds / (24 * 3600));
		seconds = seconds % (24 * 3600);
		let hour = Math.floor(seconds / 3600);
		seconds %= 3600;
		let minutes = Math.floor(seconds / 60);
		seconds %= 60;

		let string = Math.round(seconds) + 's ago';
		if (minutes > 0) string = Math.round(minutes) + 'mins ago';
		if (hour > 0) string = Math.round(hour) + 'hrs, ' + string;
		if (days > 0) string = '>24hrs ago';
		if (days > 3) string = 'Never'

		return string;
	}

	function getQueueString(ms: number) {
		let seconds = ms / 1000;
		const hours = Math.floor(seconds / 3600);
		seconds = seconds % 3600;
		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		let string: string = seconds.toString().padStart(2, '0');
		if (seconds <= 0) string = 'Soon';
		if (minutes > 0) string = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
		if (hours >= 1) string = '>1hr';
		if (hours > 2) string = '>2hrs';
		if (hours > 5) string = '>5hrs'
		if (hours > 8) string = 'Tmrw'
		return string;
	}

	var hasData = $state(false)
	var currentTimeMS: number = $state(Date.now())
	var match: string = $state('loading...');
	var queueTime: number = $state(0);
	var hasQueued = $state(false);
	var time: string = $derived(getQueueString(queueTime));
	var timerColor: string = $derived.by(() => {
		if (hasQueued) return 'red';
		else if (queueTime <= 2 * 60 * 1000) return 'yellow';
		else return 'green';
	})
	var color: string = $state('#fff');
	var lastUpdatedMS = $state(0);
	var msSinceUpdate = $derived(currentTimeMS - lastUpdatedMS)
	var lastUpdated = $derived(msToRelative(msSinceUpdate))
	var updateSource = $state('none');
    var breakAfter: string = $state('Unknown')

	async function load() {
		const res = await fetch('/api/queue');
		if (res.ok) {
			let data: formattedTimer = await res.json();
			updateSource = data.source;
			let realData = data.data;
			if (Object.keys(realData).length > 1) hasData = true;
			else hasData = false;
			({ match, queueTime, color, hasQueued } = realData);
			lastUpdatedMS = realData.dataTime;
		} else throw new Error(await res.text());
        breakAfter = (await (await fetch('/api/event')).json()).breakAfter ?? 'Unknown'
	}

	var interval: NodeJS.Timeout;
	onMount(() => {
		load();
		interval = setInterval(() => {
			queueTime -= 1000
			currentTimeMS = Date.now()
			let updateInterval = hasQueued ? 30 * 1000 : (queueTime > 60 * 1000 ? 3 * 60 * 1000 : 30 * 1000)
			if (lastUpdatedMS < Date.now() - updateInterval) load();
			if (hasQueued || queueTime < 5 * 60 * 1000) fullscreen = true
			else fullscreen = false
		}, 1000);
	});

	const data = source('/api/stream')
		.select('nexus')
		.json<formattedTimer>(({ previous }) => previous)

	$effect(() => {
		console.log(`new data:\n${Date.now()}`)
		if ($data?.source) updateSource = $data.source
		let realData = $data?.data
		if (Object.keys(realData ?? {}).length > 1 && realData) {
			({ match, queueTime, color, hasQueued } = realData);
			lastUpdatedMS = realData.dataTime;
		}
	})

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="w-screen h-screen rounded-lg border-4 border-(--white) flex justify-center items-center text-center flex-col">
	{#if hasData}
		{#if !hasQueued}
			<h1 class="text-[3rem] text-clip" style="color: var(--{color});">Queueing {match} in...</h1>
		{:else}
			<h1 class="text-[3rem] text-clip" style="color: var(--{color});">{match} On field in...</h1>
		{/if}
        <h1 class="text-[17rem] font-extrabold" style="color: var(--{timerColor});">{time}</h1>
        <div class="flex mt-0 mb-0 gap-2 items-center">
            <p class="text-[1rem] text-right text-(--grey)">{lastUpdated}</p>
			<p class="text-[1rem] text-right text-(--grey)">{updateSource}</p>
        </div>
        {#if breakAfter && breakAfter != "Unknown"}
            <h1 class="flex justify-center gap-1 text-[2.7rem]">
                Next turn around: <p class="font-medium">{breakAfter}</p>
            </h1>
        {/if}
	{:else}
		<h1 class="text-[3rem] text-clip" style="color: var(--white);">No more matches</h1>
        <h1 class="text-[17rem] font-extrabold" style="color: var(--{timerColor});">:D</h1>
        <div class="flex mt-0 mb-0 gap-2 items-center">
            <p class="text-[1rem] text-right text-(--grey)">{lastUpdated}</p>
			<p class="text-[1rem] text-right text-(--grey)"></p>
        </div>
	{/if}
</div>
