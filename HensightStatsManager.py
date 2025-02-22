from TBAData import get_matches

HensightStats = {
    "stacked_coral_event": 0,
    "average_coral_lvl": 0,
    "global_points_scored": 0,
    "average_points_permatch": 0,
    "global_penalty_points": 0,
    "event_aglee_processed": 0,
    "event_rp_earned": 0,
    "global_auto_points": 0
}

def update_stats():
    data = get_matches()
    for match in data.values():
        HensightStats["global_points_scored"] += match["alliances"]["blue"]["score"]
        HensightStats["global_points_scored"] += match["alliances"]["red"]["score"]
        for i in match["score_breakdown"].values():
            HensightStats["global_auto_points"] += i["autoPoints"]
            HensightStats["global_penalty_points"] += i["foulPoints"]

update_stats()
print(HensightStats)
