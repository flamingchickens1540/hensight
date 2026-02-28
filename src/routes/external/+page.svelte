<script>
	import { goto } from '$app/navigation';
</script>

<div class="align- m-auto flex h-67.5 w-full items-center justify-around text-7xl">
	<button
		class="rounded-xl border-10 border-[#ffb347] p-1"
		onclick={() => {
			goto('/external/stats');
		}}>Statistics</button
	>
	<button
		class="rounded-xl border-10 border-[#ffb347] p-1"
		onclick={() => {
			goto('/external/outreach');
		}}>Outreach</button
	>
</div>
