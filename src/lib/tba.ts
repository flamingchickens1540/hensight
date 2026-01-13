import { tbaKey } from '$env/static/private';

let root = 'https://www.thebluealliance.com/api/v3';

async function makeRequest(url: String) {
	const res = await fetch(root + url, {
		method: 'GET',
		headers: {
			'X-TBA-Auth-Key': tbaKey
		}
	});
	return res.json();
}

export function getEventMatches(eventKey: string) {
	return makeRequest(`/event/${eventKey}/matches`);
}

export function getEvents(year: string) {
	return makeRequest(`/events/${year}/keys`);
}
