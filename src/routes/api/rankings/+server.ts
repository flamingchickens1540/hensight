import { getEventMatches, getRankings } from '$lib/tba';
import { eventKey, team } from '$lib/config';
import { json, type RequestHandler } from '@sveltejs/kit';
import { teamData } from '$lib/nexus';

export const GET: RequestHandler = async () => {
	let tData = teamData();
	if (tData) {
		if (
			tData.myNextMatch.label.includes('Playoff') ||
			tData.myNextMatch.label.includes('Final') ||
			tData.myNextMatch.label.includes('Dummy')
		)
			return json({});
	}
	let rankings = await getRankings(eventKey);
	let formatted: { team: string; rank: number }[] = [];
	let i = 0;
	for (let rank = 0; rank < rankings.length; rank++) {
		formatted[i++] = formatRanking(rankings[rank]);
	}

	formatted.sort((a, b) => {
		return a.rank - b.rank;
	});
	return json(formatted);
};

function formatRanking(ranking: any) {
	let teamKey = ranking.team_key.split('frc')[1];
	if (teamKey == team) teamKey = `<div class="text-(--yellow) font-bold">${teamKey}</div>`;
	return {
		team: teamKey,
		rank: ranking.rank
	};
}
