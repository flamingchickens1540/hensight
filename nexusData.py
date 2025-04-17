import requests, os, time, datetime, sys, vars, tbaPulseData
from typing import Final
from dotenv import load_dotenv
from progress import progressBar
# current_event_key = 'demo5603'
# my_team_key = '100'

load_dotenv()
my_team_key = vars.team_key
current_event_key = vars.event_key_nexus
api: Final[str] = os.getenv("nexus")
url = f"https://frc.nexus/api/v1/event/{current_event_key}"

headers = {"Nexus-Api-Key": api}

def getRawData():
    response = requests.get(url, headers=headers)
    if not response.ok:
        error_message = response.text
        raise KeyError("Error getting live event status: {}".format(error_message))
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
    matches = tbaPulseData.getMatches()
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
        

count = -2
data = {}
def getNexusData():
    global count
    global data
    count+=1
    if count >= 30 or count <0 :
        count = 0
    # print('--- FILE RUN')
        startTime = time.time() * 1000
        data = getRawData()
        # print(f"Nexus Pull | Took {round((time.time()*1000) - startTime)}ms")
    startTime = time.time_ns() / 1000000
    my_team_key = vars.team_key
    pulseData = {"grow": False, "hasQueued": False}

      # Get information about a specific team's next match.   
    my_matches = filter(
        lambda m: my_team_key in m.get("redTeams", []) + m.get("blueTeams", []),
    data["matches"],
    )
    my_next_match = next(
        filter(lambda m: not m["status"] == "On field", my_matches), None
    )
    
    try: pulseData["nextMatchTeams"] = tbaPulseData.format([tbaPulseData.myNextMatch()])["all"][0]
    except ValueError: pulseData["nextMatchTeams"] = "Event key not found"
        #queueing
        
    ms = ""
    status = ""
    if my_next_match is None:
        pulseData["color"] = "#50C878"
        pulseData["queueTime"] = ":3"
        pulseData["nextMatch"] = "No more matches!"
        pulseData["bumperColor"] = "#FDF3D4"
    else:
        if my_next_match["status"] == "Queuing soon":
            pulseData["hasQueued"] = False
            type = "estimatedQueueTime"
            status = "Queueing In:"
            color = "#50C878"
        else: 
            type = "estimatedOnFieldTime"
            pulseData["hasQueued"] = True
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
        if type == "estimatedQueueTime" and s <= 300:
            color = '#FFBF00'
            pulseData["grow"] = True
        pulseData["queueTime"] = hms[2:]
        if s < 1: pulseData["queueTime"] = "Soon"
        elif s > 18000: pulseData["queueTime"] = ">5Hrs"
        elif s > 10800: pulseData["queueTime"] = ">3hrs"
        elif s > 3600: pulseData["queueTime"] = ">1hr"
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
        if ('2910' in (nowQueueFull := next(filter(lambda m: m['label'] == nowQueue, data['matches'])))['redTeams'] and '1323' in nowQueueFull['redTeams']) or ('2910' in nowQueueFull['blueTeams'] and '1323' in nowQueueFull["blueTeams"]): nowQueue = f"<p style='color: #07a000;'>{nowQueue}</p>"
    except KeyError: nowQueue = "None"
    onDeck = next(filter(lambda m: m['status'] == 'On deck', data['matches']), {'label': 'None', 'redTeams': [], 'blueTeams': []})
    onField = list(filter(lambda m: m['status'] == 'On field', data['matches']))[-1]
    if ('2910' in onDeck['redTeams'] and '1323' in onDeck['redTeams']) or ('2910' in onDeck['blueTeams'] and '1323' in onDeck['blueTeams']): onDeck['label'] = f"<p style='color: #07a000;'>{onDeck['label']}</p>"
    if ('2910' in onField['redTeams'] and '1323' in onField['redTeams']) or ('2910' in onField['blueTeams'] and '1323' in onField['blueTeams']): onField['label'] = f"<p style='color: #07a000;'>{onField['label']}</p>"
    pulseData["tasks"] = f"<p><strong>Now Queueing: </strong>{nowQueue}</p><p><strong>On Deck: </strong>{onDeck['label']}</p><p><strong>On Field: </strong>{onField['label']}</p>"
    # print(f"Data Processing | Took {round((time.time_ns() / 1000000) - startTime)}ms")
    return pulseData


getNexusData()