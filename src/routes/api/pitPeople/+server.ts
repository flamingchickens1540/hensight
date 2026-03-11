import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
	let data = {
		dataAsOfTime: Date.now(),
		timeRange: '20:00 - 8:00',
		leads: ['Zach', 'Audrey'],
		people: ['Blaze', 'Brian']
	};

	const res = await fetch('https://aldousheaf.github.io/1540.TeamSchedule/api/currentPits');
	if (res.ok) {
		const body = await res.json();
		if (body) data = body;
	}

	return json(data);
};
