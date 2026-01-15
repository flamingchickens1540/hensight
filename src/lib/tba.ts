import { tbaKey } from '$env/static/private';

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

export function filterMatches(matches: any[]) {
	let pointsScored = 0;
	let averagePointsPerMatch = 0;
	let rpEarned = 0;
	let penaltyPoints = 0;
	let autoPoints = 0;
	let matchesPlayed = matches.length;
	let feetClimbed = 0;
	let redWinCount = 0;
	let blueWinCount = 0;
	for (let match of matches) {
		pointsScored += match.alliances.blue.score;
		if (match.score_breakdown == null) continue;
		rpEarned += match.score_breakdown.blue.rp;
		rpEarned += match.score_breakdown.red.rp;
		penaltyPoints += match.score_breakdown.blue.foulPoints;
		penaltyPoints += match.score_breakdown.red.foulPoints;
		autoPoints += match.score_breakdown.red.autoPoints;
		autoPoints += match.score_breakdown.blue.autoPoints;

		if (match.score_breakdown.blue.endGameRobot1 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.blue.endGameRobot2 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.blue.endGameRobot3 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.blue.endGameRobot1 == 'ShallowCage') feetClimbed += 2.4479166667;
		else if (match.score_breakdown.blue.endGameRobot2 == 'ShallowCage') feetClimbed += 2.4479166667;
		else if (match.score_breakdown.blue.endGameRobot3 == 'ShallowCage') feetClimbed += 2.4479166667;
		else if (match.score_breakdown.red.endGameRobot1 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.red.endGameRobot2 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.red.endGameRobot3 == 'DeepCage') feetClimbed += 0.2604166667;
		else if (match.score_breakdown.red.endGameRobot1 == 'ShallowCage') feetClimbed += 2.4479166667;
		else if (match.score_breakdown.red.endGameRobot2 == 'ShallowCage') feetClimbed += 2.4479166667;
		else if (match.score_breakdown.red.endGameRobot3 == 'ShallowCage') feetClimbed += 2.4479166667;

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
