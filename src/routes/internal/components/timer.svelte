<script lang="ts">
	import { onDestroy, onMount } from 'svelte';

	const msToTime = (ms: number) => {
		return new Date(ms).toTimeString().split(' ')[0];
	};

	function getQueueString(ms: number, hasQueued: false) {
		let seconds = ms / 1000;
		const hours = Math.floor(seconds / 3600);
		seconds = seconds % 3600;
		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		let string: string = seconds.toString().padStart(2, '0');
		if (!hasQueued) {
			if (seconds <= 0) string = 'Soon';
			if (minutes > 0) string = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
			if (hours > 0) string = '>1hr';
		}
		else string = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
		return string;
	}

	var match: string = $state('loading...');
	var queueTime: number = $state(0);
	var hasQueued = $state(false);
	var time: string = $derived(getQueueString(queueTime, hasQueued));
	var timerColor: string = $derived.by(() => {
		if (hasQueued) return 'red';
		else if (queueTime < 5 * 60 * 1000) return 'yellow';
		else return 'green';
	})
	var currentTime: string = $derived(msToTime(Date.now()));
	var color: string = $state('#fff');
	let lastUpdated = Date.now();
	const interval = setInterval(() => {
		queueTime -= 1000
		if (queueTime <= 0 || lastUpdated < Date.now() - 60 * 1000) load();
	}, 1000);
	onDestroy(() => clearInterval(interval));

	async function load() {
		const res = await fetch('/api/queue');
		if (res.ok) {
			let data = await res.json();
			({ match, queueTime, color, hasQueued } = data);
			lastUpdated = Date.now();
		} else throw new Error(await res.text());
	}
	onMount(() => {
		load();
	});
</script>

<div class="size-full rounded-lg border-4 border-(--white)">
	<div class="flex items-center justify-between">
		{#if !hasQueued}
			<h1 class="p-1 text-[2.5rem]" style="color: {color};">Queueing {match} in...</h1>
		{:else}
			<h1 class="p-1 text-[2.5rem]" style="color: {color};">{match} On field in...</h1>
		{/if}
		<h1 class="p-1 text-[2.5rem]">{currentTime}</h1>
	</div>
	<div class="flex w-full h-fit justify-center pt-1">
		<h1 class="text-[10rem] font-extrabold" style="color: var(--{timerColor});">{time}</h1>
	</div>
</div>
