<script lang="ts">
	import { onDestroy, onMount } from "svelte";

	var data: {hasData: boolean; channelID: string} = $state({hasData: false, channelID: ''})
    async function load() {
        const res = await fetch("/api/livestream");
        data = await res.json();
    }
	let intverval: NodeJS.Timeout
    onMount(() => {
		load()
		const iframe = document.querySelector('iframe');
		intverval = setInterval(() => {
			if (iframe) iframe.src = iframe.src;
		}, 5 * 60 * 1000);
	})
	onDestroy(() => clearInterval(intverval))
</script>

{#if data.hasData}
	<div class="border-white size-full rounded-lg border-4">
		<iframe 
		width="100%" 
		height="100%" 
		src="https://www.youtube-nocookie.com/embed/{data.channelID}?autoplay=1&mute=1&start=99999" 
		title="YouTube video player" 
		frameborder="0" 
		allow="autoplay;" 
		referrerpolicy="strict-origin-when-cross-origin" 
		allowfullscreen
		>
		</iframe>
	</div>
{/if}