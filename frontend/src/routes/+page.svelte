<script>
	import Schedule from './schedule.svelte';
	import Timer from './timer.svelte';
	import Event from './event.svelte';
	import Announcements from './announcements.svelte';
</script>

<head>
	<title>The Holy Hen has Acquired Sight</title>
</head>

<div class="container">
	<div style="grid-area: schedule;"><Schedule></Schedule></div>
    <div style="grid-area: timer;"><Timer></Timer></div>
    <div style="grid-area: event;"><Event></Event></div>
    <div style="grid-area: announcements;"><Announcements></Announcements></div>
</div>

<style>
	.container {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(5, 1fr);
        grid-template-areas:
            "big big schedule"
            "big big schedule"
            "big big schedule"
            "announcements event timer"
            "announcements event timer";
        gap: 10px;
        width: 1920px;
        height: 1080px;
	}
</style>
