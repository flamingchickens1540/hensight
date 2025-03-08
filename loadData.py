from TBAData import load_events
import sys, os, dotenv

dotenv.load_dotenv()

genKeys = False
progress = False
for i in sys.argv:
    if i == '-k':genKeys = True
    elif i == '-p': progress = True
load_events(genKeys=genKeys, shouldProgress=progress, write=True, year=os.getenv("year"))