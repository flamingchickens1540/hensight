import statbotics

myTeam = 1540
currentYear = 2024

def getTeam():
    sb = statbotics.Statbotics()
    data = sb.get_team_year(myTeam, currentYear)
    print('Successfully got team data')
    importantData = [data['epa_end'], data['wins'], data['losses']]
    # print(importantData)
    return importantData
getTeam()
# for i in data:
#     print(i,':',data[i])

