import { timeZone } from '$lib/config';
import { json, type RequestHandler } from '@sveltejs/kit';
import { readFileSync } from 'fs';

export const GET: RequestHandler = async () => {
	let data = await getPitsPersonnelJSON();
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

function getPitsPersonnelCSV(): PitsPersonnel {
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

async function getPitsPersonnelJSON(): Promise<PitsPersonnel> {
	const res = await fetch(
		'https://raw.githubusercontent.com/AldousHeaf/1540schedule/refs/heads/main/schedule.json'
	);
	let data = await res.json();
	const nowMs = Date.now();
	const date = new Date(nowMs);

	const currentDay = date.toLocaleDateString('en-US', { weekday: 'long', timeZone: timeZone });
	for (let day of data.days) {
		if (day.label == currentDay) {
			data = day;
			break;
		}
	}

	var result: PitsPersonnel = {
		timeRange: null,
		people: [],
		leads: []
	};

	let correctSlotIndex = 0;
	for (let i = 0; i < data.timeBlocks.length; i++) {
		const [startStr, endStr] = data.timeBlocks[i].split('-');
		const [startH, startM] = startStr.split(':').map(Number);
		const [endH, endM] = endStr.split(':').map(Number);

		const slotStart = new Date(date);
		slotStart.setHours(startH, startM, 0, 0);
		const slotEnd = new Date(date);
		slotEnd.setHours(endH, endM, 0, 0);

		if (nowMs >= slotStart.getTime() && nowMs < slotEnd.getTime()) {
			correctSlotIndex = i;
			result.timeRange = data.timeBlocks[i];
		}
	}

	for (let person of data.people) {
		if (person.schedule[correctSlotIndex] == 'Pits') result.people.push(person.name);
		else if (person.schedule[correctSlotIndex] == 'Pit Lead') result.leads.push(person.name);
	}

	console.log(result);
	return result;
}
