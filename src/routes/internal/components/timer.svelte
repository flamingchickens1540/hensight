<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	let { shouldUpdate = $bindable() } = $props();

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
		if (hours > 0) string = '>1hr';
		if (hours > 2) string = '>2hrs';
		if (hours > 8) string = 'Tmrw'
		return string;
	}

	var hasData = $state(false)
	var match: string = $state('loading...');
	var queueTime: number = $state(0);
	var hasQueued = $state(false);
	var time: string = $derived(getQueueString(queueTime));
	var timerColor: string = $derived.by(() => {
		if (hasQueued) return 'red';
		else if (queueTime <= 2 * 60 * 1000) return 'yellow';
		else return 'green';
	})
	var currentTimeMS: number = $state(Date.now())
	var currentTime: string = $derived(msToTime(currentTimeMS));
	var color: string = $state('#fff');
	var lastUpdatedMS = $state(Date.now());
	var msSinceUpdate = $derived(currentTimeMS - lastUpdatedMS)
	var lastUpdated = $derived(msToRelative(msSinceUpdate))
	var es: EventSource;

	async function load() {
		const res = await fetch('/api/queue');
		if (res.ok) {
			let data = await res.json();
			if (Object.keys(data).length > 0) hasData = true;
			else hasData = false;
			({ match, queueTime, color, hasQueued } = data);
			lastUpdatedMS = Date.now();
		} else throw new Error(await res.text());
	}

	async function initStream() {
		es = new EventSource('/api/stream')
		es.onmessage = (e) => {
			let data = JSON.parse(e.data)
			if (Object.keys(data).length > 0) hasData = true;
			else hasData = false;
			({ match, queueTime, color, hasQueued } = data);
			lastUpdatedMS = Date.now();
			shouldUpdate = true;
		};
	}

	var interval: NodeJS.Timeout;
	onMount(() => {
		load();
		initStream();
		setInterval(() => {
			queueTime -= 1000
			currentTimeMS = Date.now()
			if (queueTime <= 0 || lastUpdatedMS < Date.now() - 3 * 60 * 1000) load();
		}, 1000);
	});
	onDestroy(() => {
		clearInterval(interval);
		es?.close()
	});
</script>

<div class="size-full rounded-lg border-4 border-(--white)">
	{#if hasData}
		<div class="flex items-center justify-between">
			{#if !hasQueued}
				<h1 class="pl-1 pt-1 text-[2.4rem] text-clip" style="color: var(--{color});">Queueing {match} in...</h1>
			{:else}
				<h1 class="pl-1 pt-1 text-[2.4rem] text-clip" style="color: var(--{color});">{match} On field in...</h1>
			{/if}
			<div class="flex flex-col">
				<h1 class="pr-1 pt-1 text-[2.3rem]">{currentTime}</h1>
				<p class="text-[1.5rem] text-right text-(--grey)">{lastUpdated}</p>
			</div>
		</div>
		<div class="flex w-full h-fit justify-center pt-1">
			<h1 class="text-[10rem] font-extrabold" style="color: var(--{timerColor});">{time}</h1>
		</div>
	{:else}
		<div class="flex items-center justify-between">
				<h1 class="p-1 text-[2.5rem] text-(--yellow)">No more matches</h1>
			<div class="flex flex-col">
				<h1 class="pr-1 pt-1 text-[2.3rem]">{currentTime}</h1>
				<p class="text-[1.5rem] text-right text-(--grey)">{lastUpdated}</p>
			</div>
		</div>
		<div class="flex w-full h-fit justify-center pt-1">
			<h1 class="text-[10rem] font-extrabold text-(--green)">:)</h1>
		</div>
	{/if}
</div>
