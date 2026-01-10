import { nexusKey } from '$env/static/private';
import { eventKey, team, type nexusMatch, type times } from './vars';

async function getData() {
	const response = await fetch(`https://frc.nexus/api/v1/event/${eventKey}`, {
		method: 'GET',
		headers: {
			'Nexus-Api-Key': nexusKey
		}
	});

	if (!response.ok) {
		const errorMessage = await response.text();
		// console.error('Error getting live event status:', errorMessage);
		return false;
	}

	return await response.json();
}

export async function teamData() {
	const data = await getData();
	if (!data) return false;
	const myMatches = data.matches.filter((m: nexusMatch) => m.redTeams?.includes(team) || m.blueTeams?.includes(team));
	const myNextMatch = myMatches.find((m: nexusMatch) => m.status !== 'On field');

	var allianceColor: string
	var estimatedQueueTime: number
	if (myNextMatch) {
		allianceColor = myNextMatch.redTeams?.includes(team) ? 'red' : 'blue';
		estimatedQueueTime = myNextMatch.times.estimatedQueueTime;
	}
	else {
		allianceColor = "white"
		estimatedQueueTime = -1
	}

	var formattedData: {myMatches: nexusMatch[], myNextMatch: nexusMatch, allianceColor: string, estimatedQueueTime: number}
	formattedData = {myMatches: myMatches, myNextMatch: myNextMatch, allianceColor: allianceColor, estimatedQueueTime: estimatedQueueTime}
	return formattedData;
}

export async function getAnnouncements() {
	const data = await getData();
	let announcements: {"id": string, "parts": string, "requestedByTeam": string, "postedTime": number}[] = data.announcements
    let partRequests: {"id": string, "announcements": string, "postedTime": number}[] = data.partRequests
}

export async function eventData() {
	const data = await getData();
	let nowQueue = data.nowQueuing;
	let matches = data.myMatches
	return {nowQueue, matches}
}
