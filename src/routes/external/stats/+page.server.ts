import { eventKey } from '$lib/config';
import prisma from '$lib/prisma';
import { filterMatches, getEventMatches } from '$lib/tba';
import type { PageServerLoad } from './$types';
import stats from '$lib/stats.json';
import type { statsData } from '$lib/types';

export const load: PageServerLoad = async () => {
	// const data = filterMatches(await getEventMatches(eventKey));
	const data = await prisma.event.findUnique({ where: { key: eventKey } });
	let globalData = (await prisma.event.findUnique({ where: { key: 'GLOBAL' } })) ?? {
		key: 'GLOBAL',
		pointsScored: 0,
		averagePointsPerMatch: 0,
		rpEarned: 0,
		penaltyPoints: 0,
		autoPoints: 0,
		matchesPlayed: 0,
		feetClimbed: 0
	};
	// globalData.pointsScored += data.pointsScored;
	// globalData.averagePointsPerMatch += data.averagePointsPerMatch;
	// globalData.rpEarned += data.rpEarned;
	// globalData.penaltyPoints += data.penaltyPoints;
	// globalData.autoPoints += data.autoPoints;
	// globalData.matchesPlayed += data.matchesPlayed;
	// globalData.feetClimbed += data.feetClimbed;
	stats.globalPointsScored.value = globalData?.pointsScored ?? 0;
	stats.globalPenaltyPoints.value = globalData?.penaltyPoints ?? 0;
	stats.globalMatchesPlayed.value = globalData?.matchesPlayed ?? 0;
	stats.globalPercent2Moon.value = (globalData?.feetClimbed / 1255000) * 100;
	stats.eventPointsScored.value = data?.pointsScored ?? 0;
	stats.eventAveragePointsPerMatch.value = data?.averagePointsPerMatch ?? 0;
	stats.eventRpEarned.value = data?.rpEarned ?? 0;
	stats.eventPenaltyPoints.value = data?.penaltyPoints ?? 0;
	stats.eventAutoPoints.value = data?.autoPoints ?? 0;
	stats.eventMatchesPlayed.value = data?.matchesPlayed ?? 0;
	let final = Object.values(stats);
	return { final };
};
