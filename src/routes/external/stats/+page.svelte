<script lang="ts">
	import { onMount } from "svelte";
	import type { PageProps } from "./$types";
    let { data }: PageProps = $props();

    let i = 0;
    let stats = $derived(data.final)
    let stat = $derived(stats[i])
    let p1 = $derived(stat.p1)
    let p2 = $derived(stat.p2)
    let value = $derived(stat.value.toLocaleString())

    function increment() {
        i++
        if (i>=stats.length) i = 0
        stat = stats[i]
    }

    // onMount(() => {
    //     setInterval(() => {
    //        increment()
    //     }, 5000)
    // })
</script>

<button onclick={increment} class="w-full h-67.5 m-auto text-center border-14 border-(--color-yellow)">
    <h1 class="text-[5rem]">{p1}</h1>
    <h1 class="text-[10rem] text-(--color-yellow)">{value}</h1>
    <h1 class="text-[5rem]">{p2}</h1>
</button>