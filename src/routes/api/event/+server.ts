import { eventData, teamData } from "$lib/nexus"
import type { nexusMatch } from "$lib/vars";
import { json, type RequestHandler } from "@sveltejs/kit";

const msToTime = (ms: number) => {return new Date(ms).toTimeString().split(' ')[0]}

export const GET: RequestHandler = async () => {
    let data = await eventData()
    if (!data) {
        return json({nowQueue: "Q67", onField: "Q69", lunch: "15:40"})
    }

    let nowQueuing = data.nowQueue
    if (nowQueuing.includes("Qualification")) nowQueuing = "QM"+nowQueuing.split(" ")[1]
    else if (nowQueuing.includes("Practice")) nowQueuing = "PM"+nowQueuing.split(" ")[1]

    let fileded: nexusMatch[] = data.matches.filter((m: nexusMatch) => m.status == "On field")
    fileded.sort((a, b) => {return parseInt(b.label.split(" ")[1]) - parseInt(a.label.split(" ")[1])})
    let onField = fileded[0].label
    if (onField.includes("Qualification")) onField = "QM"+onField.split(" ")[1]
    else if (onField.includes("Practice")) onField = "PM"+onField.split(" ")[1]

    let matchBeforeLunch: nexusMatch = data.matches.find((m: nexusMatch) => {m.breakAfter == "Lunch"})
    let lunchMS: number = matchBeforeLunch.times.estimatedStartTime + 3 * 60 * 1000
    let lunch = msToTime(lunchMS)

    return json({ nowQueuing, onField, lunch })
}