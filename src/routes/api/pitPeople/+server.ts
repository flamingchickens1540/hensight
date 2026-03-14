import { timeZone } from '$lib/config';
import { json, type RequestHandler } from '@sveltejs/kit';
import { readFileSync } from 'fs';

export const GET: RequestHandler = async () => {
	let data = getPitsPersonnel();
	if (data.timeRange == null) {
		data = {
			timeRange: 'Not Scheduled',
			people: ['Baseball Chuck', 'The 3D Printer'],
			leads: ['The Robot', 'Basketball Chuck']
		};
	}
	return json(data);
};

interface PitsPersonnel {
	timeRange: string | null;
	people: string[];
	leads: string[];
}

function getPitsPersonnel(): PitsPersonnel {
	let nowMs = Date.now();
	const csvText = readFileSync('static/schedule.csv', 'utf-8');

	const lines = csvText.trim().split('\n');

	let headers: string[] = [];
	const result: PitsPersonnel = { timeRange: null, people: [], leads: [] };

	for (const line of lines) {
		const cols = line.split(',');

		if (cols[0] === 'Day') {
			headers = cols;
			continue;
		}

		const day = cols[0];
		const name = cols[1];

		const date = new Date(nowMs);
		const currentDay = date.toLocaleDateString('en-US', { weekday: 'long', timeZone: timeZone });

		if (day !== currentDay) continue;

		for (let i = 2; i < headers.length; i++) {
			const [startStr, endStr] = headers[i].split('-');
			const [startH, startM] = startStr.split(':').map(Number);
			const [endH, endM] = endStr.split(':').map(Number);

			const slotStart = new Date(date);
			slotStart.setHours(startH, startM, 0, 0);

			const slotEnd = new Date(date);
			slotEnd.setHours(endH, endM, 0, 0);

			const assignment = cols[i]?.trim();

			if (nowMs >= slotStart.getTime() && nowMs < slotEnd.getTime()) {
				result.timeRange = headers[i];
				if (assignment === 'Pits') result.people.push(name);
				else if (assignment === 'Pit Lead') result.leads.push(name);
				break;
			}
		}
	}

	return result;
}
