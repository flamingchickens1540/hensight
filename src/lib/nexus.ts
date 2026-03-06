import { nexusKey } from '$env/static/private';
import { type announcement, type nexusMatch, type partRequest } from './types';
import { eventKey, team } from './config';

var data: {
	eventKey: string;
	dataAsOfTime: number;
	nowQueuing: string;
	matches: nexusMatch[];
	announcements: announcement[];
	partsRequests: partRequest[];
};

export async function updateData() {
	const response = await fetch(`https://frc.nexus/api/v1/event/${eventKey}`, {
		method: 'GET',
		headers: {
			'Nexus-Api-Key': nexusKey
		}
	});

	if (!response.ok) {
		const errorMessage = await response.text();
		console.log('Error getting live event status:', errorMessage);
		return false;
	}

	data = await response.json();
}

export function teamData() {
	if (!data) return false;
	const myMatches = data.matches.filter(
		(m: nexusMatch) => m.redTeams?.includes(team) || m.blueTeams?.includes(team)
	);
	let myNextMatch = myMatches.find((m: nexusMatch) => m.status !== 'On field');

	if (!myNextMatch)
		myNextMatch = {
			label: 'Dummy Match',
			status: 'Now queuing',
			redTeams: ['1540', '1540', '1540'],
			blueTeams: ['1844', '1844', '1844'],
			times: {
				estimatedQueueTime: Date.now(),
				estimatedOnDeckTime: Date.now(),
				estimatedOnFieldTime: Date.now(),
				estimatedStartTime: Date.now()
			},
			breakAfter: 'End of day'
		};
	let allianceColor = myNextMatch.redTeams?.includes(team) ? 'red' : 'blue';
	let estimatedQueueTime = myNextMatch.times.estimatedQueueTime;
	let estimatedOnFieldTime = myNextMatch.times.estimatedOnFieldTime;

	return {
		myMatches,
		myNextMatch,
		allianceColor,
		estimatedQueueTime,
		estimatedOnFieldTime
	};
}

export function allMatches() {
	if (!data) return false;
	return data.matches;
}

export async function getAnnouncements() {
	if (!data) return false;
	let announcements: announcement[] = data.announcements;
	let partRequests: partRequest[] = data.partsRequests;
	return { announcements, partRequests };
}

export async function eventData() {
	if (!data) return false;
	let nowQueue = data.nowQueuing;
	let tData = teamData();
	if (tData) {
		let matches = tData.myMatches;
		return { nowQueue, matches };
	} else return false;
}
