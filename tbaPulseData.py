import tbapy

key = 'Ab5I0k9SHkYT1FC4Yh5T2lpnjsewAsHNRUnoRLcnk7vueOW4VeNWf2NMBzfGsDeN'
event_key = '2024cc' #TESTING! change to your event key when using at events

tba = tbapy.TBA(key)

def getRankings():
    rankings = tba.event_rankings(event_key)
    
    top10 = []
    
    for i in rankings['rankings']:
        if i['rank'] > 15: break
        top10.append('Rank '+str(i['rank'])+': '+str(i['team_key']))
    # print(top10)
    return top10
        
getRankings()