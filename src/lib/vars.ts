export let eventKey = "2025gal"
export let year = "2025"
export let team = "1540"

export type nexusMatch = {
    "label": string,
    "status": string,
    "redTeams": string[],
    "blueTeams": string[],
    "breakAfter": string,
    "times": times
}

export type times = {
    "estimatedQueueTime": string,
    "estimatedOnDeckTime": string,
    "estimatedOnFieldTime": string,
    "estimatedStartTime": string
}