<script lang="ts">
	import { goto } from "$app/navigation";
    import { Confetti } from "svelte-confetti"
	import type { PageProps } from "./$types";
    let { data }: PageProps = $props();

    let clicks = $derived(data.clicks)
    let lastEventClicks = $derived(data.lastEventClicks)
    let globalClicks = $derived(data.globalClicks)

    let color = $derived.by(() => {
        return clicks > lastEventClicks ? 'green' : 'red';
    })
    let lastUpdatedCount = $state(0);
    let showingConfetti = $state(false);

    function click() {
        clicks++;
        globalClicks++;

        if (clicks % 1540 == 0) {
            showingConfetti = true;
            setTimeout(() => {
                showingConfetti = false
            }, 10 * 1000)
        }

        if (clicks >= lastUpdatedCount + 10) {
            lastUpdatedCount = clicks;
            fetch('/api/clicks', { method: 'POST', body: JSON.stringify({ clicks }) });
        }
    }
</script>
{#if showingConfetti}
    <div style="
    position: fixed;
    top: -5px;
    left: 0;
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    overflow: hidden;
    pointer-events: none;">
    <Confetti x={[-5, 5]} y={[0, 0.1]} delay={[0, 2000]} infinite duration={5000} amount={200} fallDistance="100vh" size={20}/>
    </div>
{/if}
<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute flex items-center justify-center flex-col gap-5">
    <button class="big-red-button" onclick={click}>Press Me</button>
    <div class="flex justify-center gap-2 text-3xl">
        <p class="font-medium" style="color: var(--{color});">Clicks Last Event: {lastEventClicks}</p>
        <h1 class="text-4xl">Clicks: {clicks}</h1>
        <p class="font-medium">Clicks all time: {globalClicks}</p>
    </div>
</div>
 <nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-3xl font-bold">
    <button
        class="rounded-xl border-4 border-(--yellow) p-1 w-[10%]"
        onclick={() => {
            goto('/external/');
        }}>Back</button
	>
  </nav>


<style>
  .big-red-button {
    background-color: var(--red);
    color: var(--white);
    font-size: 2rem;
    font-weight: bold;
    padding: 3rem 3rem;
    border: none;
    border-radius: 50%;        /* makes it circular */
    cursor: pointer;
    box-shadow: 0 8px 0 #800000,          /* bottom "depth" shadow */
                0 10px 20px rgba(0,0,0,0.4); /* outer glow */
    transition: all 0.1s ease;
  }

  .big-red-button:active {
    box-shadow: 0 2px 0 #800000,
                0 4px 10px rgba(0,0,0,0.4);
    transform: translateY(6px);  /* moves down when pressed */
  }
</style>