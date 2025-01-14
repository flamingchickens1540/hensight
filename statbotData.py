import statbotics
from main import year, my_team_key



def getTeam():
    sb = statbotics.Statbotics()
    data = sb.get_team_year(my_team_key, year)
    print("Successfully got team data")
    importantData = {
        "epa_total": data["epa_end"],
        "wins": data["wins"],
        "losses": data["losses"],
    }
    # print(importantData)
    return importantData


getTeam()
# for i in data:
#     print(i,':',data[i])
