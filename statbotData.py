import statbotics

def statbot():
    sb = statbotics.Statbotics()
    data = sb.get_team_year(1540, 2024)
    print('Successfully got team data')
    importantData = [data['epa_end'], data['wins'], data['losses']]
    print(importantData)
    return importantData
statbot()
# for i in data:
#     print(i,':',data[i])

