import { getAnnouncements } from '$lib/nexus';
import type { announcement, partRequest } from '$lib/types';
import { json, type RequestHandler } from '@sveltejs/kit';

type processedItem = {
	author: string;
	message: string;
	time: string;
};

export const GET: RequestHandler = async () => {
	const data = await getAnnouncements();
	if (!data) {
		return json([
			{
				author: 'Pit Admin',
				message: 'the pits are burning down',
				time: '15m ago'
			},
			{
				author: '1844',
				message: 'we need a 18x44 meter pizza',
				time: '40m ago'
			}
		]);
	}
	let announcements: processedItem[] = processAnnouncements(data.announcements);
	let partRequests: processedItem[] = processPartRequests(data.partRequests);

	let all: processedItem[] = [];
	all.concat(announcements, partRequests);
	return json(all);
};

function msToRelative(ms: number): string {
	let seconds = ms / 1000;
	let days = Math.floor(seconds / (24 * 3600));
	seconds = seconds % (24 * 3600);
	let hour = Math.floor(seconds / 3600);
	seconds %= 3600;
	let minutes = Math.floor(seconds / 60);
	seconds %= 60;

	let string = Math.round(seconds) + 's ago';
	if (minutes != 0) string = Math.round(minutes) + 'mins ago';
	if (hour != 0) string = Math.round(hour) + 'hrs, ' + string;
	if (days != 0) string = '>24hrs ago';

	return string;
}

function processAnnouncements(raw: announcement[]): processedItem[] {
	raw.sort((a, b) => a.postedTime - b.postedTime);
	let processed: processedItem[] = [];
	for (let announcement of raw) {
		processed.push({
			author: 'Pit Admin',
			message: announcement.announcements,
			time: msToRelative(announcement.postedTime)
		});
	}
	return processed;
}

function processPartRequests(raw: partRequest[]): processedItem[] {
	raw.sort((a, b) => a.postedTime - b.postedTime);
	let processed: processedItem[] = [];
	for (let request of raw) {
		processed.push({
			author: request.requestedByTeam,
			message: request.parts,
			time: msToRelative(request.postedTime)
		});
	}
	return processed;
}
