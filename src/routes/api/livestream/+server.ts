import { eventKey } from '$lib/config';
import { getStreamID } from '$lib/tba';
import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
	let data = {
		hasData: false,
		type: '',
		channelID: ''
	};

	const res = await getStreamID(eventKey);
	if (res) {
		data.hasData = true;
		data.channelID = res.channel;
		data.type = res.type;
	}

	return json(data);
};
