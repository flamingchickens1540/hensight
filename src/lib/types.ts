export type nexusMatch = {
    "label": string,
    "status": string,
    "redTeams": string[],
    "blueTeams": string[],
    "breakAfter": string,
    "times": times
}

export type times = {
    "estimatedQueueTime": number,
    "estimatedOnDeckTime": number,
    "estimatedOnFieldTime": number,
    "estimatedStartTime": number
}