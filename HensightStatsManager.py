from progress import progressBar
import os, dotenv, sys, vars, json, time

dotenv.load_dotenv()

def get_matches():
    with open('data.json', encoding='utf-8') as file:
        data = json.load(file)
        file.close()
        return data
    
def get_keys():
    with open('keys.json', encoding='utf-8') as file:
        keys = json.load(file)
    file.close()
    return keys

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
    "matches_played": 0,
    "matches_over_200": 0,
    "event_trough_pieces": 0,
    "tech_foul_count": 0
}

times = {
    "getKeys": 0,
    "task": [],
    "updateEvent": [],
    "lastPart": 0
}

def msdif(startTime, currentTime):
    return round((currentTime * 1000) - startTime)

def average(times):
    total = 0
    for i in times: total +=i
    return round(total/len(times), 2)

def update_stats():
    startTime = time.time() * 1000
    keys = get_keys()
    times["getKeys"] = msdif(startTime, time.time())
    for key in progressBar(keys, prefix="Updating Stats", length=0, printIterable=True):
        time1 = time.time() * 1000
        with open(f'data/{key}.json', encoding='utf-8') as file:
            data = json.load(file)
            time2 = time.time() * 1000
            updateEvent(data)
            times["updateEvent"].append(msdif(time2, time.time()))
        file.close()
        times["task"].append(msdif(time1, time.time()))
    time3 = time.time() * 1000
    try:
        HensightStats["average_points_permatch"] = round(HensightStats["points_scored"] / (HensightStats["matches_played"] * 2), 2)
    except ZeroDivisionError: HensightStats["average_points_permatch"] = 0
    # print(f"This Year: {HensightStats['points_scored']}\nLast Year: {vars.points_last_year}\nPercent: {round((HensightStats['points_scored'] / int(vars.points_last_year)) * 100, 2)}")
    HensightStats["percent_last_year"] = round((HensightStats["points_scored"] / int(vars.points_last_year)) * 100, 2)
    times["lastPart"] = msdif(time3, time.time())
    # print(f"Finished | Took {'{:,}'.format(msdif(startTime, time.time()))}ms\nGetting Keys took {'{:,}'.format(times['getKeys'])}ms\nUpdating events took {'{:,}'.format(sum(times['updateEvent']))}ms ({'{:,}'.format(average(times['updateEvent']))}ms per event on average)\nOpening/Closing files took {'{:,}'.format(sum(times['task']) - sum(times['updateEvent']))}ms\nLast Part Took {'{:,}'.format(times['lastPart'])}ms")

def update_stats_fast():
    startTime = time.time() * 1000
    keys = get_keys()
    times["getKeys"] = msdif(startTime, time.time())
    for key in progressBar(keys, prefix="Updating Stats", length=0, printIterable=True):
        time1 = time.time() * 1000
        with open(f'processedData/{key}.json', encoding='utf-8') as file:
            data = json.load(file)
            time2 = time.time() * 1000
            for i in data:
                HensightStats[i] += data[i]
            times["updateEvent"].append(msdif(time2, time.time()))
        file.close()
        times["task"].append(msdif(time1, time.time()))
    try:
        HensightStats["average_points_permatch"] = round(HensightStats["points_scored"] / (HensightStats["matches_played"] * 2), 2)
    except ZeroDivisionError: HensightStats["average_points_permatch"] = 0
    # print(f"This Year: {HensightStats['points_scored']}\nLast Year: {vars.points_last_year}\nPercent: {round((HensightStats['points_scored'] / int(vars.points_last_year)) * 100, 2)}")
    HensightStats["percent_last_year"] = round((HensightStats["points_scored"] / int(vars.points_last_year)), 2)
    # print(f"Finished | Took {'{:,}'.format(msdif(startTime, time.time()))}ms\nGetting Keys took {'{:,}'.format(times['getKeys'])}ms\nUpdating events took {'{:,}'.format(sum(times['updateEvent']))}ms ({'{:,}'.format(average(times['updateEvent']))}ms per event on average)\nOpening/Closing files took {'{:,}'.format(sum(times['task']) - sum(times['updateEvent']))}ms\nLast Part Took {'{:,}'.format(times['lastPart'])}ms")
    # print(f"Finished Product:\n{HensightStats}")

def updateEvent(data):
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
        "matches_played": 0,
        "matches_over_200": 0,
        "event_trough_pieces": 0,
        "tech_foul_count": 0
    }
    for match in data:
        HensightStats["matches_played"] +=1
        HensightStats["points_scored"] += match["alliances"]["blue"]["score"]
        HensightStats["points_scored"] += match["alliances"]["red"]["score"]
        if match["alliances"]["red"]["score"] > 200 or match["alliances"]["blue"]["score"] > 200: HensightStats["matches_over_200"] +=1
        if match["winning_alliance"] == "blue": HensightStats["blue_win_count"] +=1
        elif match["winning_alliance"] == "red": HensightStats["red_win_count"] +=1
        try:
            for i in match["score_breakdown"].values():
                HensightStats["auto_points"] += i["autoPoints"]
                HensightStats["penalty_points"] += i["foulPoints"]
                HensightStats["tech_foul_count"] += i["techFoulCount"]
        except AttributeError: pass
        if vars.event_key_tba not in match["event_key"]: continue
        try:
            for i in match["score_breakdown"].values():
                HensightStats["event_rp_earned"] += i["rp"]
                HensightStats["event_algae_processed"] += i["wallAlgaeCount"]
                HensightStats["event_trough_pieces"] += i["teleopReef"]["trough"]
        except AttributeError: pass
    return HensightStats

# update_stats()
# print(HensightStats)
