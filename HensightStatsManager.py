from TBAData import get_matches, get_keys
from progress import progressBar
import os, dotenv, sys, vars, json

dotenv.load_dotenv()

HensightStats = {
    "stacked_coral_event": 0, # to do
    "average_coral_lvl": 0, # to do
    "points_scored": 0,
    "average_points_permatch": 0,
    "penalty_points": 0,
    "event_algae_processed": 0,
    "event_rp_earned": 0,
    "auto_points": 0,
    "percent_last_year": 0,
    "blue_win_count": 0,
    "red_win_count": 0,
    "matches_played": 0
}

def update_stats():
    keys = get_keys
    for key in keys:
        with open(f'data/{key}.json', encoding='utf-8') as file:
            data = json.load(file)
        file.close()
        updateEvent(data)

def updateEvent(data):
    for match in data.values():
        HensightStats["matches_played"] +=1
        HensightStats["points_scored"] += match["alliances"]["blue"]["score"]
        HensightStats["points_scored"] += match["alliances"]["red"]["score"]
        if match["winning_alliance"] == "blue": HensightStats["blue_win_count"] +=1
        elif match["winning_alliance"] == "red": HensightStats["red_win_count"] +=1
        try:
            for i in match["score_breakdown"].values():
                HensightStats["auto_points"] += i["autoPoints"]
                HensightStats["penalty_points"] += i["foulPoints"]
        except AttributeError: pass
        if vars.event_key not in match["event_key"]: continue
        try:
            for i in match["score_breakdown"].values():
                HensightStats["event_rp_earned"] += i["rp"]
                HensightStats["event_algae_processed"] += i["wallAlgaeCount"]
        except AttributeError: pass
    try:
        HensightStats["average_points_permatch"] = round(HensightStats["points_scored"] / (HensightStats["matches_played"] * 2), 2)
    except ZeroDivisionError: HensightStats["average_points_permatch"] = 0
    HensightStats["percent_last_year"] = round((HensightStats["points_scored"] / int(vars.points_last_year)) * 100, 2)

update_stats()
# print(HensightStats)
