import { fetchData, formatTimer } from '$lib/nexus';
import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
	await fetchData();
	return json({ data: formatTimer(), source: 'poll' });
};
