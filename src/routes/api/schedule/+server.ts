import { getEventMatches } from '$lib/tba';
import { eventKey, team } from '$lib/config';
import { json, type RequestHandler } from '@sveltejs/kit';
import { allMatches, teamData } from '$lib/nexus';
import Schedule from '../../internal/components/schedule.svelte';

export const GET: RequestHandler = async () => {
	let matches = await getEventMatches(eventKey);
	let formatted: { title: string; red: string; blue: string; time: number }[] = [];
	let i = 0;
	for (let match = 0; match < matches.length; match++) {
		if (matches[match].actual_time) continue;
		formatted[i] = formatSchedule(matches[match]);
		i++;
	}
	formatted.sort((a, b) => {
		return a.time - b.time;
	});

	let tData = await teamData();
	if (!tData) return json({ percent: null, schedule: formatted });
	let myMatches = tData.myMatches;
	let complete = [];
	for (let match of myMatches) {
		if (match.status == 'On field') complete.push(match);
	}
	let percent = Math.round((complete.length / myMatches.length) * 100);

	return json({ percent, schedule: formatted });
};

function formatSchedule(match: { [k: string]: any }) {
	let title = match.key.split('_')[1].toUpperCase();
	let time = match.predicted_time;
	let red = match.alliances.red.team_keys;
	let blue = match.alliances.blue.team_keys;
	for (let i = 0; i < 3; i++) {
		red[i] = red[i].split('frc')[1];
		if (red[i] == team) red[i] = `<div class='text-(--accent-red) font-bold'>${red[i]}</div>`;
		blue[i] = blue[i].split('frc')[1];
		if (blue[i] == team) blue[i] = `<div class='text-(--accent-blue) font-bold'>${blue[i]}</div>`;
	}
	let redProcessed = `${red[0]}, ${red[1]}, ${red[2]}`;
	let blueProcessed = `${blue[0]}, ${blue[1]}, ${blue[2]}`;
	return { title: title, red: redProcessed, blue: blueProcessed, time };
}
