import { nexusWebhookToken } from '$env/static/private';
import { timeZone } from '$lib/config';
import { clients, formatTimer, setData } from '$lib/nexus';
import type { nexusData } from '$lib/types';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const token = request.headers.get('Nexus-Token');

	if (token !== nexusWebhookToken) {
		return new Response('Unauthorized', { status: 401 });
	}

	const data: nexusData = await request.json();
	console.log(
		`Recived Nexus Webhook at ${new Date(data.dataAsOfTime).toLocaleTimeString('it-IT', { timeZone: timeZone })}`
	);
	setData(data);

	for (const emit of clients) {
		console.log(`sending: ${formatTimer()}`);
		emit('nexus', JSON.stringify(formatTimer()));
	}

	return new Response('OK', { status: 200 });
};
