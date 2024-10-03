from MatchData import MatchData
class HensightStatsManager:
    def __init__(self, data):
        self.data = data
        self.current_event_data = self.data.at_event_data
        self.current_events_data = self.data.current_event_data

        self.hensight_stats = {
            "global_high_score": 0,
            "current_high_score": 0,
            "event_high_score": 0,

            "global_auto_notes": 0,
            "current_auto_notes": 0,
            "event_auto_notes": 0,

            "global_tele_notes": 0,
            "current_tele_notes": 0,
            "event_tele_notes": 0,

            "global_trap_notes": 0,
            "current_trap_notes": 0,
            "event_trap_notes": 0,

            "global_spotlight_notes": 0,
            "current_spotlight_notes": 0,
            "event_spotlight_notes": 0,
            "global_spotlight_note_percentage": 0.0,
            "current_spotlight_note_percentage": 0.0,
            "event_spotlight_note_percentage": 0.0,

            "global_speaker_notes": 0,
            "current_speaker_notes": 0,
            "event_speaker_notes": 0,

            "global_amplified_speaker_notes": 0,
            "current_amplified_speaker_notes": 0,
            "event_amplified_speaker_notes": 0,

            "global_amp_notes": 0,
            "current_amp_notes": 0,
            "event_amp_notes": 0,

            "global_total_notes": 0,
            "current_total_notes": 0,
            "event_total_notes": 0,

            "global_distance_traveled": 0,
            "current_distance_traveled": 0,
            "event_distance_traveled": 0,

            "global_red_alliance_score": 0,
            "current_red_alliance_score": 0,
            "event_red_alliance_score": 0,

            "global_blue_alliance_score": 0,
            "current_blue_alliance_score": 0,
            "event_blue_alliance_score": 0,

            "global_melody_rp": 0,
            "current_melody_rp": 0,
            "event_melody_rp": 0,

            "global_ensemble_rp": 0,
            "current_ensemble_rp": 0,
            "event_ensemble_rp": 0,

            "global_rp": 0,
            "current_rp": 0,
            "event_rp": 0,

            "global_co_op": 0,
            "current_co_op": 0,
            "event_co_op": 0
        }
    def update_stats(self):
        global_max_score = 0
        current_max_score = 0
        event_max_score = 0
        global_auto_notes = 0
        current_auto_notes = 0
        event_auto_notes = 0
        global_tele_notes = 0
        current_tele_notes = 0
        event_tele_notes = 0
        global_trap_notes = 0
        current_trap_notes = 0
        event_trap_notes = 0
        global_spotlight_notes = 0
        current_spotlight_notes = 0
        event_spotlight_notes = 0
        global_speaker_notes = 0
        current_speaker_notes = 0
        event_speaker_notes = 0
        global_amplified_speaker_notes = 0
        current_amplified_speaker_notes = 0
        event_amplified_speaker_notes = 0
        global_amp_notes = 0
        current_amp_notes = 0
        event_amp_notes = 0
        global_total_notes = 0
        current_total_notes = 0
        event_total_notes = 0
        global_distance_traveled = 0
        current_distance_traveled = 0
        event_distance_traveled = 0
        global_red_alliance_score = 0
        current_red_alliance_score = 0
        event_red_alliance_score = 0
        global_blue_alliance_score = 0
        current_blue_alliance_score = 0
        event_blue_alliance_score = 0
        global_number_of_matches = 0
        current_number_of_matches = 0
        event_number_of_matches = 0
        global_melody_rp = 0
        current_melody_rp = 0
        event_melody_rp = 0
        global_ensemble_rp = 0
        current_ensemble_rp = 0
        event_ensemble_rp = 0
        global_rp = 0
        current_rp = 0
        event_rp = 0
        global_co_op = 0
        current_co_op = 0
        event_co_op = 0

        print(self.data.event_to_match_data)
        for matches in self.data.event_to_match_data.values():
            if type(matches) != MatchData:
                for match_data in matches.values():
                    if match_data.scoringData.score_breakdown is not None:
                        global_number_of_matches = global_number_of_matches + 1
                    if match_data.maxScore > global_max_score:
                        global_max_score = match_data.maxScore
                    new_auto_notes = match_data.autoAmpNotes + match_data.autoSpeakerNotes
                    global_auto_notes = global_auto_notes + new_auto_notes
                    global_tele_notes = global_tele_notes + (match_data.totalNotes - new_auto_notes)
                    global_trap_notes = global_trap_notes + match_data.trapNotes
                    global_spotlight_notes = global_spotlight_notes + match_data.numberOfSpotlights
                    global_speaker_notes = global_speaker_notes + match_data.totalSpeakerNotes
                    global_amplified_speaker_notes = global_amplified_speaker_notes + match_data.amplifiedSpeakerNotes
                    global_amp_notes = global_amp_notes + match_data.totalAmpNotes
                    global_total_notes = global_total_notes + match_data.totalNotes
                    global_distance_traveled = global_distance_traveled + match_data.totalDistanceTraveled
                    global_red_alliance_score = global_red_alliance_score + match_data.redScore
                    global_blue_alliance_score = global_blue_alliance_score + match_data.blueScore
                    if match_data.melodyRP != 0:
                        global_melody_rp = global_melody_rp + 1
                    if match_data.ensembleRP != 0:
                        global_ensemble_rp = global_ensemble_rp + 1
                    global_rp = global_rp + match_data.totalRP
                    # global_co_op = global_co_op + match_data.coop



        for match_data in self.current_event_data.values():
            if match_data.scoringData.score_breakdown is not None:
                event_number_of_matches = event_number_of_matches + 1
            if match_data.maxScore > event_max_score:
                event_max_score = match_data.maxScore
            new_auto_notes = match_data.autoAmpNotes + match_data.autoSpeakerNotes
            event_auto_notes = event_auto_notes + new_auto_notes
            event_tele_notes = event_tele_notes + (match_data.totalNotes - new_auto_notes)
            event_trap_notes = event_trap_notes + match_data.trapNotes
            event_spotlight_notes = event_spotlight_notes + match_data.numberOfSpotlights
            event_speaker_notes = event_speaker_notes + match_data.totalSpeakerNotes
            event_amplified_speaker_notes = event_amplified_speaker_notes + match_data.amplifiedSpeakerNotes
            event_amp_notes = event_amp_notes + match_data.totalAmpNotes
            event_total_notes = event_total_notes + match_data.totalNotes
            event_distance_traveled = event_distance_traveled + match_data.totalDistanceTraveled
            event_red_alliance_score = event_red_alliance_score + match_data.redScore
            event_blue_alliance_score = event_blue_alliance_score + match_data.blueScore
            if match_data.melodyRP != 0:
                event_melody_rp = event_melody_rp + 1
            if match_data.ensembleRP != 0:
                event_ensemble_rp = event_ensemble_rp + 1
            event_rp = event_rp + match_data.totalRP
            # event_co_op = event_co_op + match_data.coop

        for matches in self.current_events_data:
            if type(matches) != MatchData:
                for match_data in matches.values():
                    if match_data.scoringData.score_breakdown is not None:
                        current_number_of_matches = current_number_of_matches + 1
                    if match_data.maxScore > current_max_score:
                        current_max_score = match_data.maxScore
                    new_auto_notes = match_data.autoAmpNotes + match_data.autoSpeakerNotes
                    current_auto_notes = current_auto_notes + new_auto_notes
                    current_tele_notes = current_tele_notes + (match_data.totalNotes - new_auto_notes)
                    current_trap_notes = current_trap_notes + match_data.trapNotes
                    current_spotlight_notes = current_spotlight_notes + match_data.numberOfSpotlights
                    current_speaker_notes = current_speaker_notes + match_data.totalSpeakerNotes
                    current_amplified_speaker_notes = current_amplified_speaker_notes + match_data.amplifiedSpeakerNotes
                    current_amp_notes = current_amp_notes + match_data.totalAmpNotes
                    current_total_notes = current_total_notes + match_data.totalNotes
                    current_distance_traveled = current_distance_traveled + match_data.totalDistanceTraveled
                    current_red_alliance_score = current_red_alliance_score + match_data.redScore
                    current_blue_alliance_score = current_blue_alliance_score + match_data.blueScore
                    if match_data.melodyRP != 0:
                        current_melody_rp = current_melody_rp + 1
                    if match_data.ensembleRP != 0:
                        current_ensemble_rp = current_ensemble_rp + 1
                    current_rp = current_rp + match_data.totalRP
                    # current_co_op = current_co_op + match_data.coop




        self.hensight_stats["global_high_score"] = global_max_score
        self.hensight_stats["current_high_score"] = current_max_score
        self.hensight_stats["event_high_score"] = event_max_score
        self.hensight_stats["global_auto_notes"] = global_auto_notes
        self.hensight_stats["current_auto_notes"] = current_auto_notes
        self.hensight_stats["event_auto_notes"] = event_auto_notes
        self.hensight_stats["global_tele_notes"] = global_tele_notes
        self.hensight_stats["current_tele_notes"] = current_tele_notes
        self.hensight_stats["event_tele_notes"] = event_tele_notes
        self.hensight_stats["global_trap_notes"] = global_trap_notes
        self.hensight_stats["current_trap_notes"] = current_trap_notes
        self.hensight_stats["event_trap_notes"] = event_trap_notes
        self.hensight_stats["global_spotlight_notes"] = global_spotlight_notes
        self.hensight_stats["current_spotlight_notes"] = current_spotlight_notes
        self.hensight_stats["event_spotlight_notes"] = event_spotlight_notes
        self.hensight_stats["global_spotlight_note_percentage"] = global_spotlight_notes / (6 * global_number_of_matches)
        if current_number_of_matches is not 0:
            self.hensight_stats["event_spotlight_note_percentage"] = event_spotlight_notes / (6 * event_number_of_matches)
        if (event_number_of_matches is not 0):
            self.hensight_stats["event_spotlight_note_percentage"] = event_spotlight_notes / (6 * event_number_of_matches)
        self.hensight_stats["global_speaker_notes"] = global_speaker_notes
        self.hensight_stats["current_speaker_notes"] = current_speaker_notes
        self.hensight_stats["event_speaker_notes"] = event_speaker_notes
        self.hensight_stats["global_amplified_speaker_notes"] = global_amplified_speaker_notes
        self.hensight_stats["current_amplified_speaker_notes"] = current_amplified_speaker_notes
        self.hensight_stats["event_amplified_speaker_notes"] = event_amplified_speaker_notes
        self.hensight_stats["global_amp_notes"] = global_amp_notes
        self.hensight_stats["current_amp_notes"] = current_amp_notes
        self.hensight_stats["event_amp_notes"] = event_amp_notes
        self.hensight_stats["global_total_notes"] = global_total_notes
        self.hensight_stats["current_total_notes"] = current_total_notes
        self.hensight_stats["event_total_notes"] = event_total_notes
        self.hensight_stats["global_distance_traveled"] = global_distance_traveled
        self.hensight_stats["current_distance_traveled"] = current_distance_traveled
        self.hensight_stats["event_distance_traveled"] = event_distance_traveled
        self.hensight_stats["global_red_alliance_score"] = global_red_alliance_score
        self.hensight_stats["current_red_alliance_score"] = current_red_alliance_score
        self.hensight_stats["event_red_alliance_score"] = event_red_alliance_score
        self.hensight_stats["global_blue_alliance_score"] = global_blue_alliance_score
        self.hensight_stats["current_blue_alliance_score"] = current_blue_alliance_score
        self.hensight_stats["event_blue_alliance_score"] = event_blue_alliance_score