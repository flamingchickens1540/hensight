<script lang="ts">
	import { onDestroy, onMount } from 'svelte';

	const msToTime = (ms: number) => {
		return new Date(ms).toTimeString().split(' ')[0];
	};

	function getQueueString(ms: number) {
		let seconds = ms / 1000;
		const hours = Math.floor(seconds / 3600);
		seconds = seconds % 3600;
		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		let string: string = seconds.toString().padStart(2, '0');
		if (seconds <= 0) string = 'Now';
		if (minutes > 0) string = `${minutes.toString().padStart(2, '0')}:${seconds}`;
		if (hours > 0) string = '>1hr';
		return string;
	}

	let currentTimeMS = $state(Date.now());
	var match: string = $state('loading...');
	var queueTime: number = $state(Date.now());
	var ms: number = $derived(queueTime - currentTimeMS);
	var time: string = $derived(getQueueString(ms));
	var currentTime: string = $derived(msToTime(currentTimeMS));
	var color: string = $state('#fff');
	let lastUpdated = Date.now();
	const interval = setInterval(() => {
		currentTimeMS = Date.now();
		if (ms < 1000 || lastUpdated < Date.now() - 60 * 1000) load();
	}, 1000);
	onDestroy(() => clearInterval(interval));

	async function load() {
		const res = await fetch('/api/queue');
		if (res.ok) {
			let data = await res.json();
			({ match, queueTime, color } = data);
			lastUpdated = Date.now();
		} else throw new Error(await res.text());
	}
	onMount(() => {
		load();
	});
</script>

<div class="size-full rounded-lg border-4 border-(--color-white)">
	<div class="flex items-center justify-between">
		<h1 class="p-1 text-[4rem]" style="color: {color};">{match}</h1>
		<h1 class="p-1 text-[3rem]">{currentTime}</h1>
	</div>
	<div class="flex size-full justify-center">
		<h1 class="text-[10rem] font-extrabold text-(--color-green)">{time}</h1>
	</div>
</div>
