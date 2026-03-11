<script>
	import { goto } from "$app/navigation";
    let { children } = $props();
</script>

<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute">
    <nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-3xl font-bold">
        <button
            class="button"
            onclick={() => {
                goto('/external/outreach/general');
            }}>General</button
	    >
        <button
            class="button"
            onclick={() => {
                goto('/external/outreach/fll');
            }}>FLL</button
	    >
        <button
            class="button"
            onclick={() => {
                goto('/external/outreach/events');
            }}>Events</button
	    >
        <button
            class="button"
            onclick={() => {
                goto('/external/outreach/bunnybots');
            }}>Bunnybots</button
	    >
        <button
            class="rounded-xl border-4 border-(--red) p-1 w-[10%]"
            onclick={() => {
                goto('/external/');
            }}>Exit</button
	    >
    </nav>
</div>

<style>
    .button {
        border-radius: 12px;
        border: 4px solid var(--yellow);
        padding: 1rem;
        width: 13%;
        transition: 1s;
    }
</style>

{@render children?.()}