<script>
	import Rankings from './components/rankings.svelte';
	import Schedule from './components/schedule.svelte';
	import Timer from './components/timer.svelte';
	import Event from './components/event.svelte';
	import Announcements from './components/announcements.svelte';
	import Stream from './components/livestream.svelte';

	let scheduleVisible = $state(true)
	
	const toggle = () => scheduleVisible = !scheduleVisible;
</script>

<head>
	<title>The Holy Hen has Acquired Sight</title>
</head>

<div class="main h-screen w-screen overflow-hidden">
	<button style="grid-area: schedule" onclick={toggle}>
		{#if scheduleVisible}
			<Schedule bind:scheduleVisible = {scheduleVisible}></Schedule>
		{:else}
			<Rankings bind:scheduleVisible = {scheduleVisible}></Rankings>
		{/if}
	</button>
	<div style="grid-area: timer;"><Timer></Timer></div>
	<div style="grid-area: event;"><Event></Event></div>
	<div style="grid-area: announcements;"><Announcements></Announcements></div>
	<!-- <div style="grid-area: big"><Stream channel="firstinspires"></Stream></div> -->
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
