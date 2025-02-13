import requests, os, time, datetime
from typing import Final
from dotenv import load_dotenv
from tbaPulseData import getMatches
# from main import current_event_key, my_team_key
current_event_key = 'demo5603'
my_team_key = '100'

load_dotenv()
api: Final[str] = os.getenv("nexus")
url = f"https://frc.nexus/api/v1/event/{current_event_key}"

headers = {"Nexus-Api-Key": api}


def genTasks():
    tasks = []
    matches = getMatches()
    matches = list(filter(lambda match : match["comp_level"] == "qm", matches))
    for match in matches:
        match["sort"] = match["key"].split("m")[1]
    matches = sorted(matches, key=lambda el: el["sort"])
    for index in range(len(matches)):
        blue = matches[index]["alliances"]["blue"]["team_keys"]
        red = matches[index]["alliances"]["red"]["team_keys"]
        myAlliance = "none"
        for i in blue: 
            i = i[3:]
            if my_team_key == i: 
                myAlliance = blue
        for i in red: 
            i = i[3:]
            if my_team_key == i: 
                myAlliance = red
        for i in myAlliance:
            if my_team_key in i: continue
            count = 0
            for j in reversed(matches[:index]):
                if i in j: 
                    count+=1
                if count == 1: 
                    tasks.append(
                        {
                            "task": f"Second Check-in with {i}",
                            "time": ":P"
                        }
                    )
                elif count == 2:
                    tasks.append(
                        {
                            "task": f"Preliminary Check-in with {i}",
                            "time": ":P"
                        }
                    )
                    break
    tasks.append(
        {
            "task": "No more tasks!",
            "time": ":P"
        }
    )
    return tasks
        


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
            pulseData["color"] = "#50C878"
            pulseData["queueTime"] = ":D"
            pulseData["nextMatch"] = "No more matches!"
        else:
            if my_next_match["status"] == "Queuing soon":
                type = "estimatedQueueTime"
                status = "Queueing In:"
                color = "#50C878"
            else: 
                type = "estimatedOnFieldTime"
                status = "On Field In:"
                color = "#D22B2B"
                
            label = my_next_match["label"]
            if "Qualification" in label:
                label = "QM "+label[14:]
            elif "Practice" in label:
                label = "PM"+label[9:]
            
            s = round(my_next_match["times"][type] / 1000) - round(time.time())
            # print(f"- {round(my_next_match["times"][type] / 1000)}\n-- {round(time.time())}\n--- {s}")
            hms = str(datetime.timedelta(seconds=s))
            if type == "estimatedQueueTime" and s <= 300: color = '#CC5500'
            pulseData["queueTime"] = hms[2:]
            pulseData["color"] = color
            pulseData["nextMatch"] = f"{label} - {status}"
            if my_team_key in my_next_match["redTeams"]: pulseData["bumperColor"] = "#D22B2B"
            elif my_team_key in my_next_match["blueTeams"]: pulseData["bumperColor"] = "7393B3"
            
        #announcements
            
        def mySort(item):
            return int(item["postedTime"])
        
        def convert(milliseconds):
            seconds = milliseconds / 1000
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            
            return f"{round(hour)}hrs, {round(minutes)}mins, {round(seconds)}s"
        
        announcements = []
        if len(data["announcements"]) + len(data["partsRequests"]) <1:
            for i in range(3):
                announcements.append({'time': '', 'announcement': 'No More Announcements', 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        elif len(data["announcements"]) + len(data["partsRequests"]) >1 and len(data["announcements"]) + len(data["partsRequests"]) <3:
            for i in data["announcements"]:
                i["requestedByTeam"] = "Pit Admin"
                i["time"] = f"{convert((time.time()*1000) - i["postedTime"])} ago"
                announcements.append(i)
            for i in data["partsRequests"]:
                i["announcement"] = i["parts"]
                i["time"] = f"{convert((time.time()*1000) - i["postedTime"])} ago"
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            announcements.append({'time': '', 'announcement': "", 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        else:
            for i in data["announcements"]:
                i["time"] = f"{convert((time.time()*1000) - i["postedTime"])} ago"
                i["requestedByTeam"] = "Pit Admin"
                announcements.append(i)
            for i in data["partsRequests"]:
                i["time"] = f"{convert((time.time()*1000) - i["postedTime"])} ago"
                i["announcement"] = i["parts"]
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            pulseData["announcements"] = announcements
            
        #tasks
        pulseData["tasks"] = genTasks()

      
    return pulseData


getNexusData()
