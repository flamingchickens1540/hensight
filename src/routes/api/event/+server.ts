import { getAllMatches, getEventData, getTeamData } from '$lib/nexus';
import type { nexusMatch } from '$lib/types';
import { json, type RequestHandler } from '@sveltejs/kit';
import { timeZone } from '$lib/config';

const msToTime = (ms: number) => {
	return new Date(ms).toLocaleTimeString('it-IT', { timeZone });
};

function msToRelative(ms: number): string {
	let seconds = ms / 1000;
	let days = Math.floor(seconds / (24 * 3600));
	seconds = seconds % (24 * 3600);
	let hour = Math.floor(seconds / 3600);
	seconds %= 3600;
	let minutes = Math.floor(seconds / 60);
	seconds %= 60;

	let string = Math.round(seconds) + 's';
	if (minutes != 0) string = Math.round(minutes) + 'mins';
	if (hour != 0) string = Math.round(hour) + 'hrs, ' + string;
	if (days != 0) string = '>24hrs';

	return string;
}

export const GET: RequestHandler = async () => {
	let data = await getEventData();
	if (!data) {
		return json({ nowQueue: 'I', break: "don't", lunch: 'know' });
	}

	let nowQueuing = data.nowQueue;
	if (!nowQueuing || nowQueuing == '') nowQueuing = 'None';
	else if (nowQueuing.includes('Qualification')) nowQueuing = 'QM' + nowQueuing.split(' ')[1];
	else if (nowQueuing.includes('Practice')) nowQueuing = 'PM' + nowQueuing.split(' ')[1];

	let breakAfter = 'Unkown';
	let tData = getTeamData();
	if (tData && tData.myFollowingMatch.label != 'Dummy Match') {
		let nextEnd = tData.myNextMatch.times.estimatedStartTime + 3 * 60 * 1000;
		let followingStart = tData.myFollowingMatch.times.estimatedQueueTime;
		if (!Number.isNaN(nextEnd) && !Number.isNaN(followingStart)) {
			let dif = followingStart - nextEnd;
			breakAfter = msToRelative(dif);
		}
	}

	let all: false | nexusMatch[] = getAllMatches();
	function findMilestone(breakType: string): number {
		if (!all) return 0;
		let matchBefore = null;
		for (let match of all) {
			if (Date.now() - match.times.estimatedStartTime > 8 * 60 * 60 * 1000) continue;
			if (match.breakAfter == breakType) matchBefore = match;
		}

		let ms = 0;
		if (matchBefore) {
			ms = matchBefore.times.estimatedStartTime + 3 * 60 * 1000;
			// ms -= 8 * 60 * 1000;
		}
		return ms;
	}

	let milestone = 'Lunch';
	let milestoneMS = 0;
	let allianceMS = findMilestone('Alliance selection');
	let lunchMS = findMilestone('Lunch');
	let eomMS = findMilestone('End of day');
	if (lunchMS > Date.now()) {
		milestone = 'Lunch';
		milestoneMS = lunchMS;
	} else if (
		allianceMS > Date.now() &&
		new Date(allianceMS).getDay() == new Date(Date.now()).getDay()
	) {
		milestone = 'Alliance selection';
		milestoneMS = allianceMS;
	} else if (eomMS > Date.now()) {
		milestone = 'Matches End';
		milestoneMS = eomMS;
	}
	let milestoneString = 'Never';
	if (milestoneMS != 0) milestoneString = msToTime(milestoneMS);

	return json({ nowQueuing, breakAfter, milestone, milestoneString });
};
