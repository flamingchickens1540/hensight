import { eventKey, pointsLastYear } from '$lib/config';
import { filterMatches, getEventMatches } from '$lib/tba';
import type { PageServerLoad } from './$types';
import stats from '$lib/stats.json';
import { getData } from '$lib/db';

interface GlobalData {
	key: string;
	pointsScored: number;
	averagePointsPerMatch: number;
	rpEarned: number;
	penaltyPoints: number;
	autoPoints: number;
	matchesPlayed: number;
	feetClimbed: number;
	redWinCount: number;
	blueWinCount: number;
}

export const load: PageServerLoad = async () => {
	const data = filterMatches(await getEventMatches(eventKey));
	let globalData: GlobalData = ((await getData('GLOBAL')) as GlobalData) ?? {
		key: 'GLOBAL',
		pointsScored: 0,
		averagePointsPerMatch: 0,
		rpEarned: 0,
		penaltyPoints: 0,
		autoPoints: 0,
		matchesPlayed: 0,
		feetClimbed: 0,
		redWinCount: 0,
		blueWinCount: 0
	};

	stats.globalPointsScored.value = globalData?.pointsScored ?? 0;
	stats.globalPenaltyPoints.value = globalData?.penaltyPoints ?? 0;
	stats.globalMatchesPlayed.value = globalData?.matchesPlayed ?? 0;
	stats.globalPercent2ISS.value = (globalData?.feetClimbed / 1320000) * 100;
	if (globalData.redWinCount > globalData.blueWinCount) {
		stats.allianceWinRate.p1 = 'The red alliance has a';
		stats.allianceWinRate.value = (globalData.redWinCount / globalData.matchesPlayed) * 100;
	} else {
		stats.allianceWinRate.p1 = 'The blue alliance has a';
		stats.allianceWinRate.value = (globalData.blueWinCount / globalData.matchesPlayed) * 100;
	}
	stats.eventPointsScored.value = data?.pointsScored ?? 0;
	stats.eventAveragePointsPerMatch.value = data?.averagePointsPerMatch ?? 0;
	stats.eventRpEarned.value = data?.rpEarned ?? 0;
	stats.eventPenaltyPoints.value = data?.penaltyPoints ?? 0;
	stats.eventAutoPoints.value = data?.autoPoints ?? 0;
	stats.eventMatchesPlayed.value = data?.matchesPlayed ?? 0;
	stats.eggsSinceKickoff.value = Math.floor(((Date.now() - 1768064400000) / 31556952000) * 270);
	stats['%lastYear'].value = (globalData?.pointsScored / pointsLastYear) * 100;
	stats.daysToChamps.value = Math.round((1777072800000 - Date.now()) / (24 * 60 * 60 * 1000));
	let final = Object.values(stats);
	final.sort(() => Math.random() - 0.5);
	return { final };
};
