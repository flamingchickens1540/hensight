<script>
	let {channel} = $props()
</script>

<div class="border-white size-full rounded-lg border-4">
	<iframe
        title="twitchstream"
		src="https://player.twitch.tv/?channel={channel}&parent=localhost"
		height="100%"
		width="100%"
	>
	</iframe>
</div>
