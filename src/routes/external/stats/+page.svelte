<script lang="ts">
	import { onMount } from "svelte";
	import type { PageProps } from "./$types";
	import { goto } from "$app/navigation";
    let { data }: PageProps = $props();

    let i = 0;
    let count = 0;
    let stats = $derived(data.final)
    let stat = $derived(stats[i])
    let p1 = $derived(stat.p1)
    let p2 = $derived(stat.p2)
    let value = $derived(stat.value.toLocaleString())

    function increment() {
        i++
        count = 0;
        if (i>=stats.length) {
            i = 0
        }
        stat = stats[i]
    }

    onMount(() => {
        setInterval(() => {
           count++
           if (count >= 5) increment()
        }, 1000)
    })
</script>

<button onclick={increment} class="w-full h-67.5 m-auto text-center border-14 border-(--yellow)">
    <h1 class="text-[5rem]">{p1}</h1>
    <h1 class="text-[10rem] text-(--yellow)">{value}</h1>
    <h1 class="text-[5rem]">{p2}</h1>
</button>
<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute">
    <nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-3xl font-bold">
        <button
            class="rounded-xl border-4 border-(--yellow) p-1 w-[10%]"
            onclick={() => {
                goto('/external/');
            }}>Back</button
	    >
    </nav>
</div>