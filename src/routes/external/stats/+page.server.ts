import { eventKey, updateData, year } from '$lib/config';
import prisma from '$lib/prisma';
import { getEventMatches, getEvents } from '$lib/tba';
import type { PageServerLoad } from './$types';
import stats from '$lib/stats.json';

export const load: PageServerLoad = async () => {
	const data = await prisma.event.findUnique({ where: { key: eventKey } });
	const globalData = await prisma.event.findUnique({ where: { key: 'GLOBAL' } });
	stats.globalPointsScored.value = globalData?.pointsScored ?? 0;
	stats.globalPenaltyPoints.value = globalData?.penaltyPoints ?? 0;
	stats.globalMatchesPlayed.value = globalData?.matchesPlayed ?? 0;
	stats.globalPercent2Moon.value = (globalData?.feetClimbed ?? 0 / 1255000) * 100;
	stats.eventPointsScored.value = data?.pointsScored ?? 0;
	stats.eventAveragePointsPerMatch.value = data?.averagePointsPerMatch ?? 0;
	stats.eventRpEarned.value = data?.rpEarned ?? 0;
	stats.eventPenaltyPoints.value = data?.penaltyPoints ?? 0;
	stats.eventAutoPoints.value = data?.autoPoints ?? 0;
	stats.eventMatchesPlayed.value = data?.matchesPlayed ?? 0;
	let final = Object.values(stats);
	return { final };
};
