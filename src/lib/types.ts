export type nexusData = {
	eventKey: string;
	dataAsOfTime: number;
	nowQueuing: string;
	matches: nexusMatch[];
	announcements: announcement[];
	partsRequests: partRequest[];
};

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

export type partRequest = {
	id: string;
	parts: string;
	requestedByTeam: string;
	postedTime: number;
};
export type announcement = { id: string; announcement: string; postedTime: number };

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

export type formattedTimer = {
	match: string;
	queueTime: number;
	color: string;
	hasQueued: boolean;
	dataTime: number;
};
