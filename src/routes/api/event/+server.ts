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
	let fileded: nexusMatch[] = [];
	let all: false | nexusMatch[] = allMatches();
	if (all) {
		for (let match of all) {
			if (match.status == 'On field') fileded.push(match);
		}
		if (fileded?.length > 0) {
			fileded.sort((a, b) => {
				return b.times.estimatedOnFieldTime - a.times.estimatedOnFieldTime;
			});
			onField = fileded[0].label;
			if (onField.includes('Qualification')) onField = 'QM' + onField.split(' ')[1];
			else if (onField.includes('Practice')) onField = 'PM' + onField.split(' ')[1];
		}
	}

	function findMilestone(breakType: string): number {
		if (!all) return 0;
		let matchBefore = null;
		for (let match of all) {
			if (match.breakAfter == breakType) matchBefore = match;
		}

		let ms = 0;
		if (matchBefore) {
			ms = matchBefore.times.estimatedStartTime + 3 * 60 * 1000;
			ms -= 8 * 60 * 1000;
		}
		return ms;
	}

	let milestone = '';
	let milestoneMS = 0;
	let lunchMS = findMilestone('Lunch');
	let eomMS = findMilestone('End of day');
	if (lunchMS > Date.now()) {
		milestone = 'Lunch';
		milestoneMS = lunchMS;
	} else if (eomMS > Date.now()) {
		milestone = 'Matches End';
		milestoneMS = eomMS;
	}
	let milestoneString = msToTime(milestoneMS);

	return json({ nowQueuing, onField, milestone, milestoneString });
};
