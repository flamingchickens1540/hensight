import tbapy, os, json, sys
from typing import Final
from dotenv import load_dotenv
from progress import progressBar

load_dotenv()
event_key: Final[str] = os.getenv("tba")
tba = tbapy.TBA(event_key)
year = '2024'

def load_events(genKeys=False, shouldProgress=False):
    keys = []
    data = {}
    print('-- Getting Match Keys')
    if genKeys:
        for i in progressBar(tba.events(year=year, keys=True), prefix='Progress: ', suffix='Complete', length=75, printIterable=True):
            for j in tba.event_matches(event=i, keys=True):
                keys.append(j)
        with open('keys.json', 'w', encoding='utf-8') as file:
            json.dump(keys, file, ensure_ascii=False, indent=4)
        file.close()
    else:
        with open('keys.json', encoding='utf-8') as file:
            keys = json.load(file)
        file.close()
    print('Done\n-- Writing Match Data')
    progress = bytes(0)
    if shouldProgress:
        file = open('progress.txt', 'rb')
        record_progress = file.read()
        file.close()
    else: record_progress = bytes(0)
    for i in progressBar(keys, prefix='Progress: ', suffix='Complete'):
        if progress < record_progress and shouldProgress:
            progress+=bytes(1)
            continue
        data[i] = tba.match(key=i)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()
        progress +=bytes(1)
        if progress > record_progress: record_progress = progress
        file = open('progress.txt', 'wb')
        file.write(record_progress)
        file.close()
    progress, record_progress = bytes(0)
    file = open('progress.txt', 'w')
    file.write(record_progress)
    file.close()

def get_matches():
    with open('data.json', encoding='utf-8') as file:
        data = json.load(file)
        file.close()
        return data

def get_match(key):
    data = get_matches()
    return data[key]

genKeys = False
progress = False
for i in sys.argv:
    if i == '-k':genKeys = True
    elif i == '-p': progress = True

load_events(genKeys, progress)