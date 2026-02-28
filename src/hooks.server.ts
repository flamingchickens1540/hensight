import { updateData } from '$lib/nexus';

let started = false;

export async function handle({ event, resolve }) {
	if (!started) {
		started = true;

		setInterval(() => {
			updateData().catch(console.error);
		}, 60_000);
	}

	return resolve(event);
}
