import { fetchData } from '$lib/nexus';

let started = false;

export async function handle({ event, resolve }) {
	if (!started) {
		started = true;

		fetchData();
		setInterval(() => {
			fetchData().catch(console.error);
		}, 60 * 1000);
	}

	return resolve(event);
}
