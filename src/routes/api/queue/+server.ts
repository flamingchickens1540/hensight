import { teamData } from "$lib/nexus"
import { json, type RequestHandler } from "@sveltejs/kit";


export const GET: RequestHandler = async () => {
    let data = await teamData()
    if (!data) {
        return json({match: "Q67", queueTime: Date.now(), color: "#ee2c2c"})
    }
    let match = data.myNextMatch.label
    if (match.includes("Qualification")) match = "QM"+match.split(" ")[1]
    else if (match.includes("Practice")) match = "PM"+match.split(" ")[1]

    let estMS: number = data.estimatedQueueTime;
    let rn = Date.now()
    let difference = rn - estMS

    let color = "#fff"
    if (data.allianceColor == 'red') color = "#ee2c2c"
    else if (data.allianceColor == 'blue') color = "#6495ed"

    return json({match, queueTime: difference, color})
}