import { produce } from 'sveltekit-sse';
import { clients } from '$lib/nexus';

export function POST() {
	return produce(function start({ emit }) {
		clients.add(emit);
		return function stop() {
			clients.delete(emit);
		};
	});
}
