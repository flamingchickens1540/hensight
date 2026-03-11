import { eventKey, lastEventKey } from '$lib/config';
import { getClicks } from '$lib/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	let clicks = await getClicks(eventKey);
	let lastEventClicks = await getClicks(lastEventKey);
	let globalClicks = await getClicks('GLOBAL');
	return { clicks, lastEventClicks, globalClicks };
};
