export type nexusMatch = {
	label: string;
	status: string;
	redTeams: string[];
	blueTeams: string[];
	breakAfter: string;
	times: times;
};

export type times = {
	estimatedQueueTime: number;
	estimatedOnDeckTime: number;
	estimatedOnFieldTime: number;
	estimatedStartTime: number;
};

export type statsData = {
	key: string;
	pointsScored: number;
	averagePointsPerMatch: number;
	rpEarned: number;
	penaltyPoints: number;
	autoPoints: number;
	matchesPlayed: number;
	feetClimbed: number;
};

export type partRequest = {
	id: string;
	parts: string;
	requestedByTeam: string;
	postedTime: number;
};
export type announcement = { id: string; announcements: string; postedTime: number };

export type statObj = {
	pointsScored: number;
	averagePointsPerMatch: number;
	rpEarned: number;
	penaltyPoints: number;
	autoPoints: number;
	matchesPlayed: number;
	feetClimbed: number;
	redWinCount: number;
	blueWinCount: number;
};
