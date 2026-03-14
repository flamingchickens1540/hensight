<script lang="ts">
	import { onMount } from "svelte";

	var data: {hasData: boolean; channelID: string} = $state({hasData: false, channelID: ''})
    async function load() {
        const res = await fetch("/api/livestream");
        data = await res.json();
		console.log(data)
    }
    onMount(load)

</script>

{#if data.hasData}
	<div class="border-white size-full rounded-lg border-4">
		<iframe 
		width="100%" 
		height="100%" 
		src="https://www.youtube-nocookie.com/embed/{data.channelID}?autoplay=1&mute=1" 
		title="YouTube video player" 
		frameborder="0" 
		allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
		referrerpolicy="strict-origin-when-cross-origin" 
		allowfullscreen
		>
		</iframe>
	</div>
{/if}