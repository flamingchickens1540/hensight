import { tbaKey } from '$env/static/private';
import { timeZone } from './config';

let root = 'https://www.thebluealliance.com/api/v3';

async function makeRequest(url: String) {
	const res = await fetch(root + url, {
		method: 'GET',
		headers: {
			'X-TBA-Auth-Key': tbaKey
		}
	});
	return res.json();
}

export function getEventMatches(eventKey: string) {
	return makeRequest(`/event/${eventKey}/matches`);
}

export function getEvents(year: string) {
	return makeRequest(`/events/${year}/keys`);
}

export async function getPastEvents(year: string) {
	const res = await makeRequest(`/events/${year}/simple`);
	let events = [];
	for (let event of res) {
		let start = event.start_date;
		if (Date.parse(start) <= Date.now()) events.push(event.key);
	}
	return events;
}

export async function getRankings(eventKey: string) {
	const res = await makeRequest(`/event/${eventKey}/rankings`);
	return res.rankings.length >= 1 ? res.rankings : false;
}

export async function getStreamID(eventKey: string) {
	const res = await makeRequest(`/event/${eventKey}`);
	let webcasts: { channel: string; date: string; type: string }[] = res.webcasts;
	if (!webcasts) return false;
	return (
		webcasts.find((stream) => stream.date == new Date().toLocaleDateString('en-US'))?.channel ??
		webcasts[0].channel
	);
}

function calcClimbFeet(depth: string) {
	if (depth == 'Level1') return 2.25;
	else if (depth == 'Level2') return 3.75;
	else if (depth == 'Level3') return 5.25;
	else return 0;
}

export function filterMatches(matches: any[]) {
	let pointsScored = 0;
	let averagePointsPerMatch = 0;
	let rpEarned = 0;
	let penaltyPoints = 0;
	let autoPoints = 0;
	let matchesPlayed = 0;
	let feetClimbed = 0;
	let redWinCount = 0;
	let blueWinCount = 0;
	for (let match of matches) {
		if (!match.actual_time) continue;
		matchesPlayed++;
		pointsScored += match.alliances.blue.score;
		pointsScored += match.alliances.red.score;
		if (!match.score_breakdown) continue;
		let blue = match.score_breakdown.blue;
		let red = match.score_breakdown.red;
		rpEarned += blue.rp;
		rpEarned += red.rp;
		penaltyPoints += blue.foulPoints;
		penaltyPoints += red.foulPoints;
		autoPoints += red.hubScore.autoPoints;
		autoPoints += blue.hubScore.autoPoints;

		feetClimbed += calcClimbFeet(red.endGameTowerRobot1);
		feetClimbed += calcClimbFeet(red.endGameTowerRobot2);
		feetClimbed += calcClimbFeet(red.endGameTowerRobot3);

		feetClimbed += calcClimbFeet(blue.endGameTowerRobot1);
		feetClimbed += calcClimbFeet(blue.endGameTowerRobot2);
		feetClimbed += calcClimbFeet(blue.endGameTowerRobot3);

		feetClimbed += calcClimbFeet(red.autoTowerRobot1);
		feetClimbed += calcClimbFeet(red.autoTowerRobot2);
		feetClimbed += calcClimbFeet(red.autoTowerRobot3);

		feetClimbed += calcClimbFeet(blue.autoTowerRobot1);
		feetClimbed += calcClimbFeet(blue.autoTowerRobot2);
		feetClimbed += calcClimbFeet(blue.autoTowerRobot3);

		if (match.winning_alliance == 'red') redWinCount++;
		else if (match.winning_alliance == 'blue') blueWinCount++;
	}
	if (matchesPlayed > 0) averagePointsPerMatch = Math.round(pointsScored / matchesPlayed);
	else averagePointsPerMatch = 0;
	return {
		pointsScored,
		averagePointsPerMatch,
		rpEarned,
		penaltyPoints,
		autoPoints,
		matchesPlayed,
		feetClimbed,
		redWinCount,
		blueWinCount
	};
}
