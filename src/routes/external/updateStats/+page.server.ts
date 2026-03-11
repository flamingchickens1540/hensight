import { year } from '$lib/config';
import { filterMatches, getEventMatches, getEvents, getPastEvents } from '$lib/tba';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import cliProgress from 'cli-progress';
import { addData } from '$lib/db';

export const load: PageServerLoad = async () => {
	console.log('Starting...');
	let eventKeys = await getPastEvents(year);
	console.log(`Recived ${eventKeys.length} event keys`);
	let globalData = {
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
	console.log('Loading from TBA...');
	let count = 0;
	const progBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
	progBar.start(eventKeys.length, 0);
	for (let key of eventKeys) {
		progBar.increment();
		const matches = await getEventMatches(key);
		if (matches.length < 1) continue;
		let data = filterMatches(matches);
		globalData.pointsScored += data.pointsScored;
		globalData.averagePointsPerMatch += data.averagePointsPerMatch;
		globalData.rpEarned += data.rpEarned;
		globalData.penaltyPoints += data.penaltyPoints;
		globalData.autoPoints += data.autoPoints;
		globalData.matchesPlayed += data.matchesPlayed;
		globalData.feetClimbed += data.feetClimbed;
		globalData.redWinCount += data.redWinCount;
		globalData.blueWinCount += data.blueWinCount;
		await addData(key, data);
		count++;
	}
	console.log(`Processed data for ${count} events`);
	await addData('GLOBAL', globalData);

	redirect(303, '/external/stats');
};
