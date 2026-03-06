<script lang="ts">
	import { onMount } from "svelte";

    let { scheduleVisible = $bindable() } = $props();

    var data: {team: string, rank: number}[] = $state([])
    async function load() {
        const res = await fetch("/api/rankings");
        data = await res.json();
    }

    var container: HTMLDivElement;
    var scrolling: boolean = false;
    var prev: boolean = true;

    onMount(() => {
        container = document.getElementById('autoScrollList') as HTMLDivElement;
        function autoScroll() {
            if (scheduleVisible || container.clientHeight >= container.scrollHeight) {
                requestAnimationFrame(autoScroll);
                return;
            }

            if (scrolling) container.scrollTop += 2;
            else {
                if (scheduleVisible != prev) setTimeout(() => scrolling = true, 2000)
                prev = scheduleVisible
            }
            
            if (container.scrollHeight > 1 && container.scrollTop + container.clientHeight >= container.scrollHeight - 1) {
                scrolling = false;
                load()
                setTimeout(() => container.scrollTop = 0, 1000)
                setTimeout(() => scheduleVisible = true, 2000);
            }

            requestAnimationFrame(autoScroll);
        }

        autoScroll();
    });

    onMount(() => {
        load()
        setInterval(load, 60 * 1000)
    })
</script>

<div class="border-4 border-white rounded-lg size-full">
    <h1 class="pt-0.5 pl-1 text-[2.5rem]">Rankings</h1>
    <div class="w-full max-h-[87%] overflow-auto scroll-smooth border-t-4 border-white" id="autoScrollList">
        {#if data.length == 0}
            <div class="text-5xl font-bold m-auto p-3 size-fit text-(--green)">No rankings D:</div>
        {:else}
            {#each data as rank}
                <div class="text-[2.5rem] text-left flex flex-row justify-left gap-2 pl-2 pb-0.5"><h1>{rank.rank}: </h1><p>{@html rank.team}</p></div>
            {/each}
        {/if}
    </div> 
</div>