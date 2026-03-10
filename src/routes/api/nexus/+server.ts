import { nexusWebhookToken } from '$env/static/private';
import { emitter, formatTimer, setData } from '$lib/nexus';
import type { nexusData } from '$lib/types';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const token = request.headers.get('Nexus-Token');

	if (token !== nexusWebhookToken) {
		return new Response('Unauthorized', { status: 401 });
	}

	const data: nexusData = await request.json();
	setData(data);

	emitter.emit('nexus', formatTimer());
	return new Response('OK', { status: 200 });
};
