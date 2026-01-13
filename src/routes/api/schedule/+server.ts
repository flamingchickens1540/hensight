import {getEventMatches} from "$lib/tba"
import {eventKey, team} from "$lib/config"
import { json, type RequestHandler } from "@sveltejs/kit";


export const GET: RequestHandler = async () => {
    let matches = await getEventMatches(eventKey)
    let formatted: {"title": string, "red": string[], "blue": string[]}[] = []
    let i = 0
    for (let match = 0; match < matches.length; match++) {
        if (matches[match].comp_level != "qm") continue
        formatted[i] = formatSchedule(matches[match])
        i++
    }
    formatted.sort((a, b) => {return parseInt(a.title.split("QM")[1]) - parseInt(b.title.split("QM")[1])})
    return json(formatted)
}

function formatSchedule(match: {[k: string]: any}) {
    let title = match.key.split("_")[1].toUpperCase()
    let red = match.alliances.red.team_keys
    let blue = match.alliances.blue.team_keys
    for (let i = 0; i<3; i++) {
        red[i] = red[i].split('frc')[1]
        blue[i] = blue[i].split('frc')[1]
    }
    return {"title": title, "red": red, "blue": blue}
}