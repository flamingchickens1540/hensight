import datetime
import requests
import sys
import time


event_key = "demo8771"  # TESTING! change to the event key before using at events
url = "https://frc.nexus/api/v1/event/" + event_key

headers = {"Nexus-Api-Key": "gckINf2G_dswez0anwAsTTGQ9Cc"}


def nexusData():
    # print('--- FILE RUN')
    response = requests.get(url, headers=headers)
    if not response.ok:
        error_message = response.text
        print("Error getting live event status: {}".format(error_message))
        sys.exit()

    data = response.json()
    print("Successfully got live event status")

    # Get information about a specific team's next match.
    my_team_number = "1000"  # TESTING! change to 1540 before using at events
    my_matches = filter(
        lambda m: my_team_number in m.get("redTeams", []) + m.get("blueTeams", []),
        data["matches"],
    )
    my_next_match = next(
        filter(lambda m: not m["status"] == "On field", my_matches), None
    )
    pulseData = []
    announcements = []
    partRequests = []
    matchInfo = ""
    formated_time = ""
    # print(data['dataAsOfTime'])
    if my_next_match:
        estimated_queue_time = my_next_match["times"].get("estimatedQueueTime", None)
        # print('queue time:',estimated_queue_time/1000)
        time_until_queue = round(estimated_queue_time / 1000 - time.time())
        # print('current time:',round(time.time()))
        # print('time untill queue: ',time_until_queue)
        if time_until_queue > 60 and time_until_queue < 3600:
            formated_time = (
                "and will queue in " + str(round(time_until_queue / 60)) + " minutes"
            )
        elif time_until_queue > 3600 and time_until_queue:
            formated_time = (
                "and will queue in "
                + str(round(time_until_queue / 3600, 1))
                + " hour(s)"
            )
        elif time_until_queue < 60 and time_until_queue > 0:
            formated_time = (
                "and will queue in " + str(round(time_until_queue)) + " secconds"
            )
        else:
            formated_time = "is queueing NOW"
        # print('--- formated time: ',formated_time)
        matchInfo = f"Team {my_team_number}'s next match is {my_next_match['label']} {formated_time}"  # .format(my_team_number, my_next_match['label'], datetime.datetime.fromtimestamp(estimated_queue_time/100).strftime('%H:%M:%S'))
        # print('--- match infO; ',matchInfo)
    else:
        matchInfo = "Team {} doesn't have any future matches scheduled yet".format(
            my_team_number
        )

    pulseData.append(matchInfo)

    # Get announcements and parts requests.
    # print(data['announcements'])
    for announcement in data["announcements"]:
        announcements.append(
            "Event announcement: {}".format(announcement["announcement"])
        )
    pulseData.append(announcements)

    for parts_request in data["partsRequests"]:
        partRequests.append(
            "Parts request for team {}: {}".format(
                parts_request["requestedByTeam"], parts_request["parts"]
            )
        )
    pulseData.append(partRequests)

    if "nowQueuing" in data:
        pulseData.append(data["nowQueuing"])
    else:
        pulseData.append("")

    my_upcomming_matches = []
    for i in data["matches"]:
        if i["status"] == "On field":
            continue
        if my_team_number in i["redTeams"] or my_team_number in i["blueTeams"]:
            my_upcomming_matches.append(i)
    if my_upcomming_matches == []:
        my_upcomming_matches = ""
    pulseData.append(my_upcomming_matches)

    # print(pulseData)
    return pulseData


nexusData()
