import time
import pickle
import multiprocessing as multip
import numpy as np

import tbaapiv3client

from MatchData import MatchData


class TBAData:
    def __init__(self):
        # API Key Authorization
        configuration = tbaapiv3client.Configuration(
            host="https://www.thebluealliance.com/api/v3",
            api_key={
                'X-TBA-Auth-Key': 'PpRS8F8YPmF2flKXvPY9S9HhzFypvmDRHR8zzBPCotpZLpsftS8rvZCdWhYB7zXN'
            }
        )

        # Get API instances
        with tbaapiv3client.ApiClient(configuration) as api_client:
            self.matches_api_instance = tbaapiv3client.EventApi(api_client)
            self.match_api_instance = tbaapiv3client.MatchApi(api_client)
            self.event_api_instance = tbaapiv3client.EventApi(api_client)

        # Set constants
        self.AT_EVENT_KEY = "2024pncmp"
        self.CURRENT_EVENT_KEYS = ["2024pncmp"]
        self.CURRENT_YEAR_KEY = "2024"
        self.EVENT_KEYS = self.event_api_instance.get_events_by_year_keys(int(self.CURRENT_YEAR_KEY))
        # self.EVENT_KEYS = self.CURRENT_EVENT_KEYS
        # Initialize Fields
        self.event_to_match_data = {}
        self.current_event_data = []
        self.at_event_data = []

    def load_events(self, file):
        print("Loading Events...")
        currentTime = time.time()

        eventsDone = 0
        totalEvents = len(self.EVENT_KEYS)

        match_to_thread = {}

        for eventKey in self.EVENT_KEYS:
            print("Requesting Event: " + eventKey)
            matches = self.get_event_matches(eventKey)
            for match in matches:
                match_to_thread[match.key] = self.match_api_instance.get_match_zebra(match.key, async_req=True)
            eventsDone = eventsDone + 1
            print(eventsDone / totalEvents * 100, "% of Events Requested")
            print("--------------------------------------------------------")
        print("Loading Event Matches Took: " + str(time.time() - currentTime))
        currentTime = time.time()
        eventsDone = 0
        for eventKey in self.EVENT_KEYS:
            self.event_to_match_data[eventKey] = {}
            for match in self.get_event_matches(eventKey):
                self.event_to_match_data[eventKey][match.key] = MatchData(match, match_to_thread[match.key].get())
            eventsDone = eventsDone + 1
            print(eventsDone / totalEvents * 100, "% of Events Loaded")
        self.current_event_data = [self.event_to_match_data[key] for key in self.CURRENT_EVENT_KEYS]

        self.at_event_data = self.event_to_match_data[self.AT_EVENT_KEY]

        print("Loading Event Matches Took: " + str(time.time() - currentTime) + " Seconds")
        print("Writing to File...")
        self.write_to_file(file)
        print("Writing to File Complete")

    def get_event_matches(self, event_key):
        matches = self.matches_api_instance.get_event_matches(event_key)
        return matches


    def write_to_file(self, file):
        dataFile = open(file, "wb")
        pickle.dump(self.event_to_match_data, dataFile)

        dataFile.close()

    def load_from_file(self, file):
        currentTime = time.time()
        print("Loading Data From File...")
        dataFile = open(file, "rb")
        self.event_to_match_data = pickle.load(dataFile)
        dataFile.close()
        self.current_event_data = [self.event_to_match_data[key] for key in self.CURRENT_EVENT_KEYS]
        self.at_event_data = self.event_to_match_data[self.AT_EVENT_KEY]
        print("Loading Data From File Complete Took: " + str(time.time() - currentTime) + " Seconds")

    def update_current_event_data(self, file):
        print("Updating Data...")
        currentTime = time.time()

        eventsDone = 0
        totalEvents = len(self.CURRENT_EVENT_KEYS)

        match_to_thread = {}

        for eventKey in self.CURRENT_EVENT_KEYS:
            print("Requesting Event: " + eventKey)
            matches = self.get_event_matches(eventKey)
            for match in matches:
                match_to_thread[match.key] = self.match_api_instance.get_match_zebra(match.key, async_req=True)
            eventsDone = eventsDone + 1
            print(eventsDone / totalEvents * 100, "% of Events Requested")
            print("--------------------------------------------------------")
        print("Loading Event Matches Took: " + str(time.time() - currentTime))
        currentTime = time.time()
        eventsDone = 0
        for eventKey in self.CURRENT_EVENT_KEYS:
            for match in self.get_event_matches(eventKey):
                self.event_to_match_data[eventKey] = {}
                self.event_to_match_data[match.key] = MatchData(match, match_to_thread[match.key].get())
            eventsDone = eventsDone + 1
            print(eventsDone / totalEvents * 100, "% of Events Loaded")
        self.current_event_data = [self.event_to_match_data[key] for key in self.CURRENT_EVENT_KEYS]

        self.at_event_data = self.event_to_match_data[self.AT_EVENT_KEY]

        print("Loading Event Matches Took: " + str(time.time() - currentTime) + " Seconds")
        print("Writing to File...")
        self.write_to_file(file)
        print("Writing to File Complete")
        print("Updated Current Event Data(took " + str(time.time() - currentTime) + " Seconds)")

    def get_match_data(self, event_key, match_key):
        return self.event_to_match_data[event_key][match_key]