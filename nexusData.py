import requests, os, time, datetime
from typing import Final
from dotenv import load_dotenv
# from main import current_event_key, my_team_key
current_event_key = 'demo5603'
my_team_key = '100'

load_dotenv()
api: Final[str] = os.getenv("nexus")
url = f"https://frc.nexus/api/v1/event/{current_event_key}"

headers = {"Nexus-Api-Key": api}


def getNexusData():
    # print('--- FILE RUN')
    response = requests.get(url, headers=headers)
    if not response.ok:
        error_message = response.text
        print("Error getting live event status: {}".format(error_message))
        pulseData = {}
        pulseData["queueTime"] = 'No nexus at this event :('
        return pulseData

    else:
        data = response.json()
        pulseData = {}
        print("Successfully got live event status")

      # Get information about a specific team's next match.
        my_matches = filter(
            lambda m: my_team_key in m.get("redTeams", []) + m.get("blueTeams", []),
        data["matches"],
        )
        my_next_match = next(
            filter(lambda m: not m["status"] == "On field", my_matches), None
        )
        
        #queueing
        
        ms = ""
        status = ""
        if my_next_match is None:
            pulseData["color"] = "green"
            pulseData["queueTime"] = ":D"
            pulseData["nextMatch"] = "No more matches!"
        else:
            if my_next_match["status"] == "Queuing soon":
                type = "estimatedQueueTime"
                status = "Queueing In:"
                color = "green"
            else: 
                type = "estimatedOnFieldTime"
                status = "On Field In:"
                color = "red"
            s = round(my_next_match["times"][type] / 1000) - round(time.time())
            # print(f"- {round(my_next_match["times"][type] / 1000)}\n-- {round(time.time())}\n--- {s}")
            hms = str(datetime.timedelta(seconds=s))
            if type == "estimatedQueueTime" and s <= 300: color = 'yellow'
            pulseData["queueTime"] = hms[2:]
            pulseData["color"] = color
            pulseData["nextMatch"] = f"{my_next_match["label"]} - {status}"
            if my_team_key in my_next_match["redTeams"]: pulseData["bumperColor"] = "#D22B2B"
            elif my_team_key in my_next_match["blueTeams"]: pulseData["bumperColor"] = "7393B3"
            
        #announcements
            
        def mySort(item):
            return int(item["postedTime"])
        
        announcements = []
        if len(data["announcements"]) + len(data["partsRequests"]) <1:
            for i in range(3):
                announcements.append({'postedTime': '', 'announcement': 'No Announcements at this time.', 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        elif len(data["announcements"]) + len(data["partsRequests"]) >1 and len(data["announcements"]) + len(data["partsRequests"]) <3:
            for i in data["announcements"]:
                i["requestedByTeam"] = "Pit Admin"
                announcements.append(i)
            for i in data["partsRequests"]:
                i["announcement"] = i["parts"]
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            announcements.append({'postedTime': '', 'announcement': "", 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        else:
            for i in data["announcements"]:
                i["requestedByTeam"] = "Pit Admin"
                announcements.append(i)
            for i in data["partsRequests"]:
                i["announcement"] = i["parts"]
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            pulseData["announcements"] = announcements
            
        #tasks
        tasks = []
        tasks.append(
            {
                "task": f"No more tasks!",
                "time": f":P"
            }
        )
        tasks.append(
            {
                "task": "this is another task!",
                "time": "right now "
            }
        )
        pulseData["tasks"] = tasks

      
    return pulseData


getNexusData()
