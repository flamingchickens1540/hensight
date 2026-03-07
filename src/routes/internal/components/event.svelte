<script lang="ts">
	import { onMount } from "svelte";

	let nowQueue = $state("Loading...")
	let breakAfter = $state("Loading...")
	let milestone = $state("Loading...")
	let milestoneTime = $state("")
    async function load() {
        const res = await fetch("/api/event");
        const data = await res.json();
		nowQueue = data.nowQueuing
		breakAfter = data.breakAfter
		milestone = data.milestone
		milestoneTime = data.milestoneString
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
		<h1 class="flex justify-center gap-1 text-[2.7rem]">
			Break After Next: <p class="font-medium">{breakAfter}</p>
		</h1>
		<h1 class="flex justify-center gap-1">
			{milestone}: <p class="font-medium">{milestoneTime}</p>
		</h1>
	</div>
</div>
