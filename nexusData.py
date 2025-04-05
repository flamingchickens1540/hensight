import requests, os, time, datetime, sys, vars
from typing import Final
from dotenv import load_dotenv
from tbaPulseData import getMatches
from progress import progressBar
# current_event_key = 'demo5603'
# my_team_key = '100'

load_dotenv()
my_team_key = vars.team_key
current_event_key = vars.event_key
api: Final[str] = os.getenv("nexus")
url = f"https://frc.nexus/api/v1/event/{current_event_key}"

headers = {"Nexus-Api-Key": api}

def getRawData():
    response = requests.get(url, headers=headers)
    if not response.ok:
        error_message = response.text
        print("Error getting live event status: {}".format(error_message))
    else: return response.json()

def getNexusMatch(TBAMatch, data):
    matches = data["matches"]
    if TBAMatch["comp_level"] == "qm": label = f'Qualification {TBAMatch["key"].split("qm")[1]}'
    elif TBAMatch["comp_level"] == "pm": label = f'Practice {TBAMatch["key"].split("qm")[1]}'
    else: raise NotImplementedError("Only quals and practice works rn :(")
    for match in matches:
        if match["label"] == label: 
            return match
    raise KeyError(f"Match Key not found in nexus. Key: {label}")

def genTasks():
    data = getRawData()
    my_team_key = vars.team_key
    tasks = []
    matches = getMatches()
    matches = list(filter(lambda match : match["comp_level"] == "qm", matches))
    for match in matches:
        match["sort"] = match["key"].split("m")[1]
    matches = sorted(matches, key=lambda el: el["sort"])
    for index in range(len(matches)):
        blue = matches[index]["alliances"]["blue"]["team_keys"]
        red = matches[index]["alliances"]["red"]["team_keys"]
        myAlliance = None
        for i in range(len(blue)): 
            blue[i] = blue[i][3:]
            if my_team_key == blue[i]: 
                myAlliance = blue
        for i in range(len(red)): 
            red[i] = red[i][3:]
            if my_team_key == red[i]: 
                myAlliance = red
        if myAlliance == None: continue
        for i in myAlliance:
            if my_team_key in i: continue
            # print("running on "+i)
            count = 0
            for j in reversed(matches[:index]):
                # if j["winning_alliance"] != None: continue
                k = j["alliances"]["red"]["team_keys"]
                l = j["alliances"]["blue"]["team_keys"]
                if i in k: 
                    count+=1
                elif i in l:
                    count+=1
                if count == 1: 
                    timeUntil = round(((getNexusMatch(j, data)["times"]["estimatedStartTime"]/1000) - time.time()) / 60)+10
                    if timeUntil > -10 and timeUntil < 30: tasks.append(
                        {
                            "task": f'<h2 class="announcement">Second Check-in with {i} after QM{j["key"].split("m")[1]}</h2>',
                            "time": timeUntil
                        }
                    )
                    count+=1
                elif count == 3:
                    timeUntil = round(((getNexusMatch(j, data)["times"]["estimatedStartTime"]/1000) - time.time()) / 60)+10
                    if timeUntil > -10 and timeUntil < 30: tasks.append(
                        {
                            "task": f'<h2 class="announcement">Preliminary Check-in with {i} after QM{j["key"].split("m")[1]}</h2>',
                            "time": timeUntil
                        }
                    )
                    break
    if len(tasks) == 0:
        tasks.append(
            {
                "task": "<h2 class='announcement' style='font-size: 3rem;'>No tasks!</h2>",
                "time": ":P"
            }
        )
    tasks = sorted(tasks, key=lambda el: el["time"])
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
        my_team_key = vars.team_key
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
            pulseData["queueTime"] = ":3"
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
            
            try: s = round(my_next_match["times"][type] / 1000) - round(time.time()) - vars.offset
            except KeyError: s = round(my_next_match["times"]["scheduledStartTime"] / 1000) - round(time.time()) - vars.offset
            # print(f"- {round(my_next_match["times"][type] / 1000)}\n-- {round(time.time())}\n--- {s}")
            hms = str(datetime.timedelta(seconds=s))
            if type == "estimatedQueueTime" and s <= 300: color = '#FFBF00'
            pulseData["queueTime"] = hms[2:]
            if s < 1: pulseData["queueTime"] = "Soon"
            elif s > 3600: pulseData["queueTime"] = "1hr+"
            pulseData["color"] = color
            pulseData["nextMatch"] = f"{label} - {status}"
            if my_team_key in my_next_match["redTeams"]: pulseData["bumperColor"] = "#D22B2B"
            elif my_team_key in my_next_match["blueTeams"]: pulseData["bumperColor"] = "#6495ED"
            if s > 36000:
                pulseData["color"] = "#50C878"
                pulseData["queueTime"] = ":3"
                pulseData["nextMatch"] = "No more matches!"
            pulseData["hidden"] = round(my_next_match["times"][type] / 100)
            
        #announcements
            
        def mySort(item):
            return int(item["postedTime"])
        
        def convert(milliseconds):
            seconds = milliseconds / 1000
            days = seconds // (24 * 3600)
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            
            string = f"{round(seconds)}s"
            if minutes != 0: string = f"{round(minutes)}mins"
            if hour != 0: string = f"{round(hour)}hrs, {string}"
            if days != 0: string = f"{round(days)} days, {string}"
            
            return string
        
        announcements = []
        if len(data["announcements"]) + len(data["partsRequests"]) <1:
            for i in range(3):
                announcements.append({'time': '', 'announcement': 'No More Announcements', 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        elif len(data["announcements"]) + len(data["partsRequests"]) >1 and len(data["announcements"]) + len(data["partsRequests"]) <3:
            for i in data["announcements"]:
                i["requestedByTeam"] = "Pit Admin"
                i["time"] = f'{convert((time.time()*1000) - i["postedTime"])} ago'
                announcements.append(i)
            for i in data["partsRequests"]:
                i["announcement"] = i["parts"]
                i["time"] = f'{convert((time.time()*1000) - i["postedTime"])} ago'
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            announcements.append({'time': '', 'announcement': "", 'requestedByTeam': ''})
            pulseData["announcements"] = announcements
        else:
            for i in data["announcements"]:
                i["time"] = f'{convert((time.time()*1000) - i["postedTime"])} ago'
                i["requestedByTeam"] = "Pit Admin"
                announcements.append(i)
            for i in data["partsRequests"]:
                i["time"] = f'{convert((time.time()*1000) - i["postedTime"])} ago'
                i["announcement"] = i["parts"]
                announcements.append(i)
            announcements.sort(key=mySort, reverse=True)
            pulseData["announcements"] = announcements
            
        #tasks
        # pulseData["tasks"] = genTasks()
        try:
            nowQueue = data['nowQueuing']
        except KeyError: nowQueue = "None"
        pulseData["tasks"] = f"<p><strong>Now Queueing: </strong>{nowQueue}</p><p><strong>On Deck: </strong>{next(filter(lambda m: m['status'] == 'On deck', data['matches']), 'None')['label']}</p><p><strong>On Field: </strong>{list(filter(lambda m: m['status'] == 'On field', data['matches']))[-1]['label']}</p>"

      
    return pulseData


getNexusData()
