import { teamData } from "$lib/nexus"
import { json, type RequestHandler } from "@sveltejs/kit";


export const GET: RequestHandler = async () => {
    let data = await teamData()
    let match = data.myNextMatch.label
    if (match.includes("Qualification")) match = "QM"+match.split(" ")[1]
    else if (match.includes("Practice")) match = "PM"+match.split(" ")[1]

    let estMS: number = data.estimatedQueueTime;
    let rn = Date.now()
    let difference = rn - estMS
    let stringTime: string
    if (difference > 1000 * 60 * 60) stringTime = ">60mins"
    else stringTime = msToHMS(difference)
    let stringCurrentTime = msToHMS(rn)

    let color = data.allianceColor;

    return json({match: match, time: stringTime, seconds: difference, color: color, currentTime: stringCurrentTime})
}