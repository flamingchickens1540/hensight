<script lang="ts">
	import { onMount } from "svelte";

    let { scheduleVisible = $bindable() } = $props();

    var schedule: {title: string, red: string, blue: string, time: number}[] = $state([])
    var percent = $state(0)
    async function load() {
        const res = await fetch("/api/schedule");
        const data = await res.json();
        percent = data.percent;
        schedule = data.schedule;
    }

    var ticking = false;

    function tick() {
        if (scheduleVisible && !ticking) {
            ticking = true;
            setTimeout(() => {
                scheduleVisible = false; 
                ticking = false;
            }, 30 * 1000)
        }
    }

    onMount(() => {
        load()
        setInterval(tick, 1000)
        setInterval(load, 60 * 1000)
    })
</script>

<div class="border-4 border-white rounded-lg size-full">
    <h1 class="text-[2.5rem]">Schedule</h1>
    <p class="text[2.2rem]">We have played {percent}% of our matches</p>
    <div class="w-full max-h-[87%] overflow-scroll border-t-4 border-white">
        {#if schedule.length == 0}
            <div class="text-5xl font-bold m-auto p-3 size-fit text-(--green)">No more matches :p</div>
        {:else}
            {#each schedule as match}
                <div class="text-[1.8rem] text-left flex flex-row justify-around"><h1>{match.title}: </h1><p class="text-(--red) flex gap-0.5">{@html match.red}</p><p class="text-(--blue) flex gap-0.5">{@html match.blue}</p></div>
            {/each}
        {/if}
    </div> 
</div>