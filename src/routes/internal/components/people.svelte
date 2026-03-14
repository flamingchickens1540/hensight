<script lang="ts">
	import { onMount } from "svelte";

	let leads = $state(["Loading..."])
    let people = $state(["Loading..."])
    let timeRange = $state("Loading...")

    async function load() {
        const res = await fetch("/api/pitPeople");
        const data = await res.json();
        leads = data.leads;
		people = data.people;
        timeRange = data.timeRange;
    }
    onMount(() => {
        load()
		setInterval(load, 1000)
    })
</script>

<div class="size-full rounded-lg border-4 border-white">
	<div class="flex flex-col gap-1 text-4xl size-full justify-around items-center m-auto">
        <h1 class="pl-1 text-[2.5rem] text-left w-full">Pits: {timeRange}</h1>
        <h2>Pit Leads</h2>
        <div class="flex gap-1">
            {#each leads as person}
            <p>{person}</p>
            {/each}
        </div>
        <h2>Pit Members</h2>
        <div class="flex gap-1">
            {#each people as person}
            <p>{person}</p>
            {/each}
        </div>
    </div>
</div>
