from TBAData import *
import sys, os, dotenv, vars, HensightStatsManager

dotenv.load_dotenv()

genKeys = False
progress = False
for i in sys.argv:
    if i == '-k':genKeys = True
    elif i == '-p': progress = True
# load_events(genKeys=genKeys, shouldProgress=progress, write=True, year=vars.year)
# fast_events(genKeys=genKeys, shouldProgress=progress, write=True, year=vars.year)

super_fast_events(genKeys=genKeys, write=True, year=vars.year)
HensightStatsManager.update_stats_fast()

# printTotalPointsLastYear()