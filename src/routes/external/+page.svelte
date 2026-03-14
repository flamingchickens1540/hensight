<script>
	import { goto } from '$app/navigation';

	function openFullScreen() {
		document.documentElement.requestFullscreen();
	}
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="w-full h-screen flex flex-col items-center justify-center gap-10 overflow-hidden" onclick={openFullScreen}>
	<div class="glass p-5 text-center">
		<h1 class="text-[10rem] text-(--yellow) font-extrabold">Hensight</h1>
		<h2 class="text-6xl text-(--light-grey) font-bold">By Team 1540</h2>
	</div>
	<div id="menu" class="glass">
		<button
			class="rounded-xl border-10 border-[#ffb347] p-1"
			onclick={() => {
				goto('/external/stats');
			}}>Statistics</button
		>
		<button
			class="rounded-xl border-10 border-[#ffb347] p-1"
			onclick={() => {
				goto('/external/cad');
			}}>CAD</button
		>
		<!-- <button
			class="rounded-xl border-10 border-[#ffb347] p-1"
			onclick={() => {
				goto('/external/outreach');
			}}>Outreach</button
		> -->
		<button
			class="rounded-xl border-10 border-[#800000] p-1"
			onclick={() => {
				goto('/external/button');
			}}>The Button</button
		>
	</div>	
</div>


<div id="bg"></div>

<style>
	#bg {
		position: absolute;
		top: 0;
		width: 60%;
		height: 100dvh;
		transform: rotate(13.494deg);
		aspect-ratio: 1/1;
		background: url(/src/lib/assets/images/1540-logo.png) var(--black) 50% / cover no-repeat;
		filter: blur(5px);
		z-index: -10;
	}

	#menu {
		width: 80%;
		height: 30%;
		font-size: 3.75rem;
		display: flex;
		align-items: center;
		justify-content: space-around;
	}

	.glass {
		background: rgba(28, 28, 28, 0.65);
		border-radius: 16px;
		box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
		backdrop-filter: blur(7.2px);
		-webkit-backdrop-filter: blur(7.2px);
		border: 1px solid rgba(28, 28, 28, 0.55);
	}
</style>