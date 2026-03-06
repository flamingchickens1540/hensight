import { updateData } from '$lib/nexus';

let started = false;

export async function handle({ event, resolve }) {
	if (!started) {
		started = true;

		updateData();
		setInterval(
			() => {
				updateData().catch(console.error);
			},
			3 * 60 * 1000
		);
	}

	return resolve(event);
}
