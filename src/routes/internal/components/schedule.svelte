<script lang="ts">
	import { onMount } from "svelte";

    let { scheduleVisible = $bindable() } = $props();

    var data: {title: string, red: string, blue: string, time: number}[] = $state([])
    async function load() {
        const res = await fetch("/api/schedule");
        data = await res.json();
    }

    var ticking = false;

    function tick() {
        if (scheduleVisible && !ticking) {
            ticking = true;
            setTimeout(() => {
                scheduleVisible = false; 
                ticking = false;
            }, 15 * 1000)
        }
    }

    onMount(() => {
        load()
        setInterval(tick, 1000)
        setInterval(load, 60 * 1000)
    })
</script>

<div class="border-4 border-white rounded-lg size-full">
    <h1 class="pt-0.5 pl-1 text-[2.5rem]">Schedule</h1>
    <div class="w-full max-h-[87%] overflow-scroll border-t-4 border-white">
        {#if data.length == 0}
            <div class="text-5xl font-bold m-auto p-3 size-fit text-(--green)">No more matches :p</div>
        {:else}
            {#each data as match}
                <div class="text-[1.9rem] text-left flex flex-row justify-around"><h1>{match.title}: </h1><p class="text-(--red) flex gap-0.5">{@html match.red}</p><p class="text-(--blue) flex gap-0.5">{@html match.blue}</p></div>
            {/each}
        {/if}
    </div> 
</div>