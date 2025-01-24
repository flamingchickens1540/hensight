import tbapy
import os
from typing import Final
from dotenv import load_dotenv
# from main import event_key
event_key = '2024cc'

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


def getPrediction():
    prediction = tba.event_predictions(event_key)
    # print(prediction)
    return prediction

getRankings()
