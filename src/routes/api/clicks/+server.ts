import { setClicks } from '$lib/db';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const data = await request.json();
	setClicks(data.clicks);
	return new Response('OK', { status: 200 });
};
