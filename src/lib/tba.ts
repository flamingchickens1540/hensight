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

function calcClimbFeet(depth: string) {
	if (depth == 'DeepCage') return 0.2604166667;
	else if (depth == 'ShallowCage') return 2.4479166667;
	else return 0;
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

		let blue = match.score_breakdown.blue;
		let red = match.score_breakdown.red;
		feetClimbed += calcClimbFeet(red.endGameRobot1);
		feetClimbed += calcClimbFeet(red.endGameRobot2);
		feetClimbed += calcClimbFeet(red.endGameRobot3);

		feetClimbed += calcClimbFeet(blue.endGameRobot1);
		feetClimbed += calcClimbFeet(blue.endGameRobot2);
		feetClimbed += calcClimbFeet(blue.endGameRobot3);

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
