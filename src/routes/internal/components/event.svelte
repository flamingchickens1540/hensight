<script lang="ts">
	import { onMount } from "svelte";

	let nowQueue = $state("Loading...")
	let onField = $state("Loading...")
	let lunch = $state("Loading...")
    async function load() {
        const res = await fetch("/api/event");
        const data = await res.json();
		nowQueue = data.nowQueuing
		onField = data.onField
		lunch = data.lunch
    }
    onMount(() => {
        load()
		setInterval(load, 60 * 1000)
    })
</script>

<div class="size-full rounded-lg border-4 border-white">
	<h1 class="p-1 text-[2.5rem]">Event</h1>
	<div class="m-auto flex w-[95%] flex-col justify-center gap-1 text-center text-[3rem]">
		<h1 class="flex justify-center gap-1">
			Now Queueing: <p class="font-medium">{nowQueue}</p>
		</h1>
		<h1 class="flex justify-center gap-1">
			On Field: <p class="font-medium">{onField}</p>
		</h1>
		<h1 class="flex justify-center gap-1">
			Lunch: <p class="font-medium">{lunch}</p>
		</h1>
	</div>
</div>
