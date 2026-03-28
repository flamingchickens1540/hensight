import { eventKey } from '$lib/config';
import { getStreamID } from '$lib/tba';
import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
	let data = {
		hasData: false,
		channelID: ''
	};

	const res = await getStreamID(eventKey);
	if (res) {
		data.hasData = true;
		data.channelID = res;
	}
	console.log(data);

	return json(data);
};
