import { allMatches, eventData, teamData } from '$lib/nexus';
import type { nexusMatch } from '$lib/types';
import { json, type RequestHandler } from '@sveltejs/kit';

const msToTime = (ms: number) => {
	return new Date(ms).toTimeString().split(' ')[0];
};

export const GET: RequestHandler = async () => {
	let data = await eventData();
	if (!data) {
		return json({ nowQueue: 'I', onField: "don't", lunch: 'know' });
	}

	let nowQueuing = data.nowQueue;
	if (!nowQueuing || nowQueuing == '') nowQueuing = 'None';
	else if (nowQueuing.includes('Qualification')) nowQueuing = 'QM' + nowQueuing.split(' ')[1];
	else if (nowQueuing.includes('Practice')) nowQueuing = 'PM' + nowQueuing.split(' ')[1];

	let onField = 'None';
	let fileded: nexusMatch[] = data.matches.filter((m: nexusMatch) => m.status == 'On field');
	if (fileded?.length > 0) {
		fileded.sort((a, b) => {
			return parseInt(b.label.split(' ')[1]) - parseInt(a.label.split(' ')[1]);
		});
		onField = fileded[0].label;
		if (onField.includes('Qualification')) onField = 'QM' + onField.split(' ')[1];
		else if (onField.includes('Practice')) onField = 'PM' + onField.split(' ')[1];
	}

	let all = allMatches();
	let matchBeforeLunch;
	if (all) {
		for (let match of all) {
			if (match.breakAfter == 'Lunch') matchBeforeLunch = match;
		}
	}
	let lunch = 'Never';
	if (matchBeforeLunch) {
		let lunchMS: number = matchBeforeLunch.times.estimatedStartTime + 3 * 60 * 1000;
		lunch = msToTime(lunchMS);
	}

	return json({ nowQueuing, onField, lunch });
};
