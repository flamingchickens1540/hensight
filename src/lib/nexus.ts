import { nexusKey } from '$env/static/private';
import { eventKey, team, type nexusMatch } from './vars';

async function getData() {
	const response = await fetch(`https://frc.nexus/api/v1/event/${eventKey}`, {
		method: 'GET',
		headers: {
			'Nexus-Api-Key': nexusKey
		}
	});

	if (!response.ok) {
		const errorMessage = await response.text();
		console.error('Error getting live event status:', errorMessage);
		return;
	}

	return await response.json();
}

async function teamData() {
	const data = await getData();
	const myMatches = data.matches.filter((m: nexusMatch) => m.redTeams?.includes(team) || m.blueTeams?.includes(team));
	const myNextMatch = myMatches.find((m: nexusMatch) => m.status !== 'On field');

	if (myNextMatch) {
		const allianceColor = myNextMatch.redTeams?.includes(team) ? 'red' : 'blue';
		const estimatedQueueTime = myNextMatch.times.estimatedQueueTime;
}

async function getAnnouncements() {
	const data = await getData();
	let announcements: {"id": string, "parts": string, "requestedByTeam": string, "postedTime": number}[] = data.announcements
    let partRequests: {"id": string, "announcements": string, "postedTime": number}[] = data.partRequests
}
