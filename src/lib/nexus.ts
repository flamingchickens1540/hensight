import { nexusKey } from '$env/static/private';
import { type announcement, type nexusData, type nexusMatch, type partRequest } from './types';
import { eventKey, team } from './config';

export const clients: Set<(eventName: string, data: string) => void> = new Set();
var data: nexusData;

export async function fetchData() {
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

export function getData() {
	if (data) return data;
	else return false;
}

export function setData(newData: nexusData) {
	if (data && newData.dataAsOfTime < data.dataAsOfTime) return;
	if (newData.eventKey != eventKey) return;

	data = newData;
}

export function getTeamData() {
	if (!data) return false;
	const myMatches = data.matches.filter(
		(m: nexusMatch) => m.redTeams?.includes(team) || m.blueTeams?.includes(team)
	);
	let myNextMatch = myMatches.find((m: nexusMatch) => m.status !== 'On field');
	let myFollowingMatch = myMatches.find(
		(m: nexusMatch) => m.status !== 'On field' && m.label !== myNextMatch?.label
	);

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
	if (!myFollowingMatch)
		myFollowingMatch = {
			label: 'Dummy Match',
			status: 'Queuing Soon',
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
		myFollowingMatch,
		allianceColor,
		estimatedQueueTime,
		estimatedOnFieldTime
	};
}

export function getAllMatches() {
	if (!data) return false;
	return data.matches;
}

export async function getAnnouncements() {
	if (!data) return false;
	let announcements: announcement[] = data.announcements;
	let partRequests: partRequest[] = data.partsRequests;
	return { announcements, partRequests };
}

export async function getEventData() {
	if (!data) return false;
	let nowQueue = data.nowQueuing;
	let tData = getTeamData();
	if (tData) {
		let matches = tData.myMatches;
		return { nowQueue, matches };
	} else return false;
}

export function formatTimer() {
	let data = getTeamData();
	if (!data || data.myNextMatch.label == 'Dummy Match') {
		return {};
	}

	let match = data.myNextMatch.label;
	if (match.includes('Qualification')) match = 'QM' + match.split(' ')[1];
	else if (match.includes('Practice')) match = 'PM' + match.split(' ')[1];

	let hasQueued = false;
	let estMS: number = 0;
	if (data.myNextMatch.status == 'Queuing soon') {
		estMS = data.estimatedQueueTime;
	} else {
		hasQueued = true;
		estMS = data.estimatedOnFieldTime;
	}
	let rn = Date.now();
	let difference = estMS - rn;

	return { match, queueTime: difference, color: data.allianceColor, hasQueued };
}
