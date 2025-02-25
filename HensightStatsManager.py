from TBAData import get_matches
from progress import progressBar
import os, dotenv

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
    data = get_matches()
    for match in data.values():
        HensightStats["matches_played"] +=1
        HensightStats["points_scored"] += match["alliances"]["blue"]["score"]
        HensightStats["points_scored"] += match["alliances"]["red"]["score"]
        if match["winning_alliance"] == "blue": HensightStats["blue_win_count"] +=1
        elif match["winning_alliance"] == "red": HensightStats["red_win_count"] +=1
        for i in match["score_breakdown"].values():
            HensightStats["auto_points"] += i["autoPoints"]
            HensightStats["penalty_points"] += i["foulPoints"]
        if os.getenv("event_key") not in match["event_key"]: continue
        for i in match["score_breakdown"].values():
            HensightStats["event_rp_earned"] += i["rp"]
            HensightStats["event_algae_processed"] += i["wallAlgaeCount"]
    HensightStats["average_points_permatch"] = round(HensightStats["points_scored"] / (HensightStats["matches_played"] * 2), 2)
    HensightStats["percent_last_year"] = round((HensightStats["points_scored"] / int(os.getenv("points_last_year"))) * 100, 2)

update_stats()
print(HensightStats)
