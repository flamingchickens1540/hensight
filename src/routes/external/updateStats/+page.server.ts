import { year } from '$lib/config';
import prisma from '$lib/prisma';
import { getEventMatches, getEvents } from '$lib/tba';
import type { PageServerLoad } from './$types';
import cliProgress from 'cli-progress';

export const load: PageServerLoad = async () => {
	let eventKeys = await getEvents(year);
	let globalData = {
		key: 'GLOBAL',
		pointsScored: 0,
		averagePointsPerMatch: 0,
		rpEarned: 0,
		penaltyPoints: 0,
		autoPoints: 0,
		matchesPlayed: 0,
		feetClimbed: 0
	};
	console.log('Loading from TBA...');
	const progBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
	progBar.start(eventKeys.length, 0);
	for (let key of eventKeys) {
		progBar.increment();
		let data = filterMatches(await getEventMatches(key));

		globalData.pointsScored += data.pointsScored;
		globalData.averagePointsPerMatch += data.averagePointsPerMatch;
		globalData.rpEarned += data.rpEarned;
		globalData.penaltyPoints += data.penaltyPoints;
		globalData.autoPoints += data.autoPoints;
		globalData.matchesPlayed += data.matchesPlayed;
		globalData.feetClimbed += data.feetClimbed;

		await prisma.event.upsert({
			where: { key },
			update: data,
			create: { key, ...data }
		});
	}
	await prisma.event.upsert({
		where: { key: 'GLOBAL' },
		update: globalData,
		create: globalData
	});
};

function filterMatches(matches: any[]) {
	let pointsScored = 0;
	let averagePointsPerMatch = 0;
	let rpEarned = 0;
	let penaltyPoints = 0;
	let autoPoints = 0;
	let matchesPlayed = matches.length;
	let feetClimbed = 0;
	for (let match of matches) {
		let score = match.alliances.red.score;
		pointsScored += match.alliances.blue.score;
		if (match.score_breakdown == null) continue;
		rpEarned += match.score_breakdown.blue.rp;
		rpEarned += match.score_breakdown.red.rp;
		penaltyPoints += match.score_breakdown.blue.foulPoints;
		penaltyPoints += match.score_breakdown.red.foulPoints;
		autoPoints += match.score_breakdown.red.autoPoints;
		autoPoints += match.score_breakdown.blue.autoPoints;
		// TODO: add feetClimbed
	}
	averagePointsPerMatch = pointsScored / matchesPlayed;
	return {
		pointsScored,
		averagePointsPerMatch,
		rpEarned,
		penaltyPoints,
		autoPoints,
		matchesPlayed,
		feetClimbed
	};
}
