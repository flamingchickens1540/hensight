import tbapy, os, time
from typing import Final
from dotenv import load_dotenv
from progress import progressBar
# from main import event_key

load_dotenv()
key: Final[str] = os.getenv("tba")
event_key = "2025orore"
my_team_key = os.getenv("team_key")

tba = tbapy.TBA(key)


def getMatches():
    return tba.event_matches(event=event_key, simple=True)

def getRankings():
    rankings = tba.event_rankings(event_key)

    top10 = []

    for i in rankings["rankings"]:
        if i["rank"] > 20:
            break
        i["team_key"] = i["team_key"][3:]
        if my_team_key in str(i["team_key"]):
            i["team_key"] = f'<strong style="color: #f6b14b;">{i["team_key"]}</strong>'
        top10.append(f'<p style="font-size: 2rem; line-height:0; height:fit-content;">Rank {str(i["rank"])}: {str(i["team_key"])}</p>')
    # print(top10)
    return top10

def myMatches():
    matches = tba.event_matches(event=event_key, simple=True)
    my_matches = []
    for match in matches:
        for i in match["alliances"]["blue"]["team_keys"]: 
            if my_team_key in i: my_matches.append(match)
        for i in match["alliances"]["red"]["team_keys"]:
            if my_team_key in i: my_matches.append(match)
    my_matches = filter(lambda match : match["comp_level"] == "qm", my_matches)
    my_matches = sorted(my_matches, key=lambda el: el["key"].split("m")[1])
    return my_matches

def myNextMatch():
    all = myMatches()
    upcoming = []
    for i in all:
        if "winning_alliance" not in i: upcoming.append(i)
    upcoming = filter(lambda match : match["comp_level"] == "qm", upcoming)
    upcoming = sorted(upcoming, key=lambda el: el["key"].split("m")[1])
    if len(upcoming) > 1: return upcoming[0]
    else: return all[len(all)-1]
    
    

def myAlliance(match):
    blue = match["alliances"]["blue"]["team_keys"]
    red  = match["alliances"]["red"]["team_keys"]
    for i in blue: 
        if my_team_key in i: return "blue"
    for i in red:
        if my_team_key in i: return "red"
    return "err"

def format(list):
    postFormat = []
    list = filter(lambda match : match["comp_level"] == "qm", list)
    list = sorted(list, key=lambda el: int(el["key"].split("m")[1]))
    for match in list:
        blue = match["alliances"]["blue"]["team_keys"]
        red  = match["alliances"]["red"]["team_keys"]

        for i in range(len(blue)):
            blue[i] = blue[i][3:]
            if my_team_key in blue[i]: blue[i] = f"<strong><u style='color: #89CFF0;'>{blue[i]}</u></strong>" #highlight your teamkey
            if "1844" in blue[i]: blue[i] = f"<strong><u>{blue[i]}</u></strong>"
            # if blue[i] in "".join(myNextMatch()["alliances"][myAlliance(myNextMatch())]["team_keys"]):
                # blue[i] = f"<strong><u>{blue[i]}</u></strong>"
        for i in range(len(red)): 
            red[i] = red[i][3:]
            if my_team_key in red[i]: red[i] = f"<strong><u style='color: #EE4B2B;'>{red[i]}</u></strong>"
            if "1844" in red[i]: red[i] = f"<strong><u>{red[i]}</u></strong>"

            # if red[i] in "".join(myNextMatch()["alliances"][myAlliance(myNextMatch())]["team_keys"]): 
                # red[i] = f"<strong><u>{red[i]}</u></strong>"

        postFormat.append(f"<div class='schedulelement'><p style='text-align: right;'>{(match['key'][10:]).upper()}: </p><p style='text-align: center;' class='red'>{red[0]}, {red[1]}, {red[2]}</p><p style='text-align: left;' class='blue'>{blue[0]}, {blue[1]}, {blue[2]}</p></div>")
    return postFormat
    

def getMatchSchedule():
    matches = tba.event_matches(event=event_key, simple=True)
    allMatches = format(matches)
    futureMatches = []
    for i in matches:
        if i["winning_alliance"] == "": futureMatches.append(i)
    if len(futureMatches) > 0: futureMatches = format(futureMatches)
    # print(futureMatches[0], "\n")
    data = {
        "all": allMatches,
        "future": futureMatches
    }
    return data

def getPrediction():
    prediction = tba.event_predictions(event_key)
    # print(prediction)
    return prediction

# getMatchSchedule()
# print(tba.event_matches(event=event_key, simple=True)[0])
