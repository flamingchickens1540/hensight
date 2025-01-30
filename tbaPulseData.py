import tbapy
import os
from typing import Final
from dotenv import load_dotenv
# from main import event_key
event_key = '2024cc'
my_team_key = '1540'

load_dotenv()
key: Final[str] = os.getenv("tba")

tba = tbapy.TBA(key)


def getRankings():
    rankings = tba.event_rankings(event_key)

    top10 = []

    for i in rankings["rankings"]:
        if i["rank"] > 20:
            break
        top10.append("Rank " + str(i["rank"]) + ": " + str(i["team_key"]))
    # print(top10)
    return top10

def format(matches):
    list = []
    for i in matches:
        blue = i["alliances"]["blue"]["team_keys"]
        red = i["alliances"]["red"]["team_keys"]
        for j in range(len(red)):
            red[j] = red[j][3:]
            if my_team_key in red[j]: red[j] = f"<strong><u>{red[j]}</u></strong>"
        for j in range(len(blue)):
            blue[j] = blue[j][3:]
            if my_team_key in blue[j]: blue[j] = f"<strong><u>{blue[j]}</u></strong>"
        list.append(f"<div class='schedulelement'><p style='text-align: right;'>{(i["key"][7:]).upper()}: </p><p style='text-align: center;' class='red'>{red[0]}, {red[1]}, {red[2]}</p><p style='text-align: left;' class='blue'>{blue[0]}, {blue[1]}, {blue[2]}</p></div>")
    return list

def getMatchSchedule():
    matches = tba.event_matches(event=event_key, simple=True)
    allMatches = [format(matches)]
    futureMatches = []
    for i in matches:
        if "score_breakdown" not in i: futureMatches.append(i)
    futureMatches = [format(futureMatches)]
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
print(tba.event_matches(event=event_key, simple=True)[0])
