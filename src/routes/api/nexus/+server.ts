import { nexusWebhookToken } from '$env/static/private';
import { clients, formatTimer, setData } from '$lib/nexus';
import type { nexusData } from '$lib/types';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const token = request.headers.get('Nexus-Token');

	if (token !== nexusWebhookToken) {
		return new Response('Unauthorized', { status: 401 });
	}

	const data: nexusData = await request.json();
	setData(data);
	console.log('new thing: ', data.dataAsOfTime);

	for (const emit of clients) {
		emit('nexus', JSON.stringify(formatTimer()));
	}

	return new Response('OK', { status: 200 });
};
