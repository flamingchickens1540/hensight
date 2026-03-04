<script>
	import { goto } from "$app/navigation";
    let { children } = $props();
</script>

<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute">
    <nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-2xl font-bold">
        <button
            class="rounded-xl border-4 border-(--yellow) p-1 w-[10%]"
            onclick={() => {
                goto('/external/outreach/thing1');
            }}>Thing 1</button
	    >
        <button
            class="rounded-xl border-4 border-(--yellow) p-1 w-[10%]"
            onclick={() => {
                goto('/external/outreach/thing2');
            }}>Thing 2</button
	    >
        <button
            class="rounded-xl border-4 border-(--yellow) p-1 w-[10%]"
            onclick={() => {
                goto('/external/outreach/thing3');
            }}>Thing 3</button
	    >
        <button
            class="rounded-xl border-4 border-(--red) p-1 w-[10%]"
            onclick={() => {
                goto('/external/');
            }}>Exit</button
	    >
    </nav>
</div>

{@render children?.()}