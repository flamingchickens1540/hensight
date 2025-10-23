import tbapy, os, dotenv
from vars import *

dotenv.load_dotenv()
TBA_KEY = os.getenv("tbaKey")
tba = tbapy.TBA(TBA_KEY)

matches = tba.event_matches(currentEvent, True)

def getSchedule():
    futureMatches = []
    for match in matches:
        if match["comp_level"] != currentPhase: continue
        # if match["winning_alliance"] == "" or match["winning_alliance"] == None: futureMatches.append(match)
        futureMatches.append(match)
    formattedMatches = []
    for match in futureMatches:
        key = match["key"][len(currentEvent)+1:]
        key = key.upper()
        redTeams = []
        for team in match["alliances"]["red"]["team_keys"]:
            redTeams.append(team[3:])
        blueTeams = []
        for team in match["alliances"]["blue"]["team_keys"]:
            blueTeams.append(team[3:])
        data = {
            "title": key,
            "red": redTeams,
            "blue": blueTeams
        }
        formattedMatches.append(data)
    return formattedMatches