import tbapy, os, json, sys, vars, HensightStatsManager
from typing import Final
from dotenv import load_dotenv
from progress import progressBar
load_dotenv()
api_key: Final[str] = os.getenv("tba")
tba = tbapy.TBA(api_key)
thisYear = vars.year

def super_fast_events(year, genKeys=False, write=True):
    print(f"Keys: {genKeys}\nWrite: {write}\nYear: {year}")
    keys = []
    if genKeys:
        print('-- Getting Event Keys')
        for i in progressBar(tba.events(year=year, keys=True)):
            keys.append(i)
        if write:
            with open('keys.json', 'w', encoding='utf-8') as file:
                json.dump(keys, file, ensure_ascii=False, indent=4)
            file.close()
    else:
        with open('keys.json', encoding='utf-8') as file:
            keys = json.load(file)
        file.close()
    print('Done\n-- Writing Match Data')
    for key in progressBar(keys):
        rawData = tba.event_matches(event=key)
        processedData = HensightStatsManager.updateEvent(rawData)
        file = open(f'processedData/{key}.json', 'w', encoding='utf-8')
        json.dump(processedData, file, ensure_ascii=False, indent=4)
        file.close()

def fast_events(year, genKeys=False, write=False, shouldProgress=False):
    print(f"Keys: {genKeys}\nWrite: {write}\nProgress: {shouldProgress}\nYear: {year}")
    keys = []
    data = {}
    if genKeys:
        print('-- Getting Event Keys')
        for i in progressBar(tba.events(year=year, keys=True)):
            keys.append(i)
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
    for i in progressBar(keys):
        if write: file = open(f"data/{i}.json", "w")
        if progress < record_progress and shouldProgress:
            progress+=bytes(1)
            continue
        for j in tba.event_matches(i):
            data[j["key"]] = j
        if write: json.dump(data, file, ensure_ascii=False, indent=4)
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
    
def update_this_event():
    rawData = tba.event_matches(event=vars.event_key_tba)
    processedData = HensightStatsManager.updateEvent(rawData)
    file = open(f'processedData/{vars.event_key_tba}.json', 'w', encoding='utf-8')
    json.dump(processedData, file, ensure_ascii=False, indent=4)
    file.close()
    # with open('data.json', encoding='utf-8') as file:
    #     data = json.load(file)
    # file.close()
    # for i in tba.event_matches(vars.event_key_tba):
    #     data[i["key"]] = i
    # with open('data.json', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)
    # file.close()
    
    # try:
    #     data = {}
    #     with open(f'data/{vars.event_key_tba}.json', encoding='utf-8') as file:
    #         for i in progressBar(tba.event_matches(vars.event_key_tba)):
    #             data[i["key"]] = i
    #         json.dump(data, file, ensure_ascii=False, indent=4)
    #     file.close()
    # except FileNotFoundError: return


def printTotalPointsLastYear():
    data = fast_events(year=vars.last_year, genKeys=True, write=False, shouldProgress=False)
    points = 0
    print("-- Finding Points")
    for match in progressBar(data.values()):
        points += match["alliances"]["blue"]["score"]
        points += match["alliances"]["red"]["score"]
    print(points)

def get_match(key):
    data = HensightStatsManager.get_matches()
    return data[key]

def getEvent(key):
    with open(f'data/{key}.json', encoding='utf-8') as file:
        data = json.load(file)
    file.close()
    return data