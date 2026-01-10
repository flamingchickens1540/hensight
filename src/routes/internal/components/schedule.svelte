<script lang="ts">
	import { onMount } from "svelte";

    var data: {title: string, red: string[], blue: string[]}[] = []
    async function load() {
        const res = await fetch("/api/schedule");
        data = await res.json();
    }
    onMount(() => {
        load()
    })
</script>

<div class="border-4 border-white rounded-lg size-full overflow-auto">
    <h1 class="p-1 text-[2.5rem]">Schedule</h1>
    {#each data as match}
        <div class="text-[1.9rem] text-justify flex flex-row justify-evenly"><h1>{match.title}: </h1><p class="text-(--color-red)">{match.red}</p><p class="text-(--color-blue)">{match.blue}</p></div>
    {/each}
</div>