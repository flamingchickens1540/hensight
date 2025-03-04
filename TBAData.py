import tbapy, os, json, sys
from typing import Final
from dotenv import load_dotenv
from progress import progressBar

load_dotenv()
api_key: Final[str] = os.getenv("tba")
tba = tbapy.TBA(api_key)
thisYear = os.getenv("year")

def load_events(year, genKeys=False, write=False, shouldProgress=False):
    keys = []
    data = {}
    print('-- Getting Match Keys')
    if genKeys:
        for i in progressBar(tba.events(year=year, keys=True), prefix='Progress: ', suffix='Complete', length=75, printIterable=True):
            for j in tba.event_matches(event=i, keys=True):
                if j != "Error": keys.append(j)
        if write:
            with open('keys.json', 'w', encoding='utf-8') as file:
                json.dump(keys, file, ensure_ascii=False, indent=4)
            file.close()
    else:
        with open('keys.json', encoding='utf-8') as file:
            keys = json.load(file)
        file.close()
    print('Done\n-- Writing Match Data')
    progress = bytes(0)
    type = 'w'
    if shouldProgress:
        file = open('progress.txt', 'rb')
        record_progress = file.read()
        file.close()
        type = 'a'
    else: record_progress = bytes(0)
    for i in progressBar(keys, prefix='Progress: ', suffix='Complete'):
        if progress < record_progress and shouldProgress:
            progress+=bytes(1)
            continue
        data[i] = tba.match(key=i)
        if write:
            with open('data.json', type, encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            file.close()
        progress +=bytes(1)
        if progress > record_progress: record_progress = progress
        if write:
            file = open('progress.txt', 'wb')
            file.write(record_progress)
            file.close()
    progress, record_progress = bytes(0), bytes(0)
    file = open('progress.txt', 'wb')
    if write: file.write(record_progress)
    file.close()
    if not write: return data
    print("Done")

def get_matches():
    print("!-- Current working directory: ", os.getcwd())
    with open('data.json', encoding='utf-8') as file:
        data = json.load(file)
        file.close()
        return data

def printTotalPointsLastYear():
    data = load_events(year=os.getenv("last_year"), genKeys=True, write=False, shouldProgress=False)
    points = 0
    for match in data.values():
        points += match["alliances"]["blue"]["score"]
        points += match["alliances"]["red"]["score"]
    print(points)

def get_match(key):
    data = get_matches()
    return data[key]
  

genKeys = False
progress = False
for i in sys.argv:
    if i == '-k':genKeys = True
    elif i == '-p': progress = True
# load_events(genKeys=genKeys, shouldProgress=progress, write=True, year=os.getenv("year"))
# printTotalPointsLastYear()
