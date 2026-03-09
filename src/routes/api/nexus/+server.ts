import { nexusWebhookToken } from '$env/static/private';
import { eventKey } from '$lib/config';
import { emitter, formatTimer, getData, getTeamData, setData } from '$lib/nexus';
import type { nexusMatch, nexusWebhookData } from '$lib/types';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const token = request.headers.get('Nexus-Token');

	if (token !== nexusWebhookToken) {
		return new Response('Unauthorized', { status: 401 });
	}

	const data: nexusWebhookData = await request.json();
	processData(data);
	emitter.emit('nexus', formatTimer());
	console.log('Nexus webhook received:', data);

	return new Response('OK', { status: 200 });
};

function processData(newMatch: nexusWebhookData) {
	const data = getData();
	if (data.dataAsOfTime > newMatch.dataAsOfTime) return;
	if (newMatch.eventKey != eventKey) return;

	let index = data.matches.findIndex((m: nexusMatch) => m.label == newMatch.match.label);

	if (index !== -1) {
		data.matches[index] = newMatch.match;
	} else {
		data.matches.push(newMatch.match);
		data.matches.sort((a, b) => a.times.estimatedQueueTime - b.times.estimatedOnDeckTime);
	}

	setData(data);
}
