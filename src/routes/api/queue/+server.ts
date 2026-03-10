import { formatTimer } from '$lib/nexus';
import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
	return json(formatTimer());
};
