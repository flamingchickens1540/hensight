<script lang="ts">
    import { onMount } from "svelte";

    var match: string = $state('loading...')
    var time: string = $state(':D')
    var secconds: number = $state(0)
    var color: string = $state('#fff')
    var currentTime: string = $state('15:40')

    async function load() {
        const res = await fetch("/api/queue");
        let data = await res.json();
        ({match, time, secconds, color, currentTime} = data)
    }
    onMount(() => {
        load()
    })

    setInterval(() => {
        currentTime = msToHMS(Date.now())
    }, 1000)
</script>

<div class="border-4 border-(--color-white) rounded-lg size-full">
    <div class="flex justify-between items-center"><h1 class="text-[4rem] p-1 text-(--color-${color})">{match}</h1><h1 class="text-[3rem] p-1">{currentTime}</h1></div>
    <div class="size-full flex justify-center"><h1 class="text-[10rem] text-(--color-green) font-extrabold">{time}</h1></div>
</div>