<script lang="ts">
    import { onMount } from "svelte";

	var data: {author: string, message: string, time: string, sort: number}[] = []
    async function load() {
        const res = await fetch("/api/announcements");
        data = await res.json();
    }
    onMount(() => {
        load()
        setInterval(load, 60 * 1000)
    })
</script>

<div class="border-4 border-white rounded-lg size-full overflow-auto">
    <h1 class="p-1 text-[2.5rem]">Announcements</h1>
    {#each data as msg}
        <div class="border-3 border-white rounded-lg w-[80%] m-auto mb-1">
            <h1 class="text-[1.4rem] p-0.5">{msg.author}</h1>
            <p class="m-auto text-center text-[1.8rem]">{msg.message}</p>
            <p class="text-(--light-grey) text-[1.2rem] pl-0.5">{msg.time}</p>
        </div>
    {/each}
</div>