import numpy as np
from tbaapiv3client import Zebra


def getTeamDistance(team):
    teamX = team.xs
    teamY = team.ys
    teamDistance = 0
    i = 0
    while i < len(teamX) - 1:
        nextIndex = i + 1
        while nextIndex + 1 < len(teamX) - 1 and (
            teamX[i] is None
            or teamY[i] is None
            or teamX[nextIndex] is None
            or teamY[nextIndex] is None
        ):
            nextIndex = nextIndex + 1
        if not (
            teamX[i] is None
            or teamY[i] is None
            or teamX[nextIndex] is None
            or teamY[nextIndex] is None
        ):
            teamDistance = teamDistance + np.hypot(
                teamX[nextIndex] - teamX[i], teamY[nextIndex] - teamY[i]
            )
        i = nextIndex
    return teamDistance


class MatchData:
    def __init__(self, match, zebraData):
        self.matchKey = match.key
        self.scoringData = match
        scoreBreakdown = self.scoringData.score_breakdown
        self.zebraData = zebraData
        self.totalDistanceTraveled = 0
        if scoreBreakdown is not None:
            red = scoreBreakdown["red"]
            blue = scoreBreakdown["blue"]
            self.autoAmpNotes = red["autoAmpNoteCount"] + blue["autoAmpNoteCount"]
            self.autoSpeakerNotes = (
                red["autoSpeakerNoteCount"] + blue["autoSpeakerNoteCount"]
            )
            self.teleAmpNotes = red["teleopAmpNoteCount"] + blue["teleopAmpNoteCount"]
            self.teleSpeakerNotes = (
                red["teleopSpeakerNoteCount"] + blue["teleopSpeakerNoteCount"]
            )
            self.trapNotes = (red["endGameNoteInTrapPoints"] / 5) + (
                blue["endGameNoteInTrapPoints"] / 5
            )
            self.amplifiedSpeakerNotes = (
                red["teleopSpeakerNoteAmplifiedCount"]
                + blue["teleopSpeakerNoteAmplifiedCount"]
            )
            self.numberOfSpotlights = 0
            if red["micCenterStage"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1
            if red["micStageLeft"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1
            if red["micStageRight"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1
            if blue["micCenterStage"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1
            if blue["micStageLeft"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1
            if blue["micStageRight"]:
                self.numberOfSpotlights = self.numberOfSpotlights + 1

            self.redScore = red["totalPoints"]
            self.blueScore = blue["totalPoints"]
            self.maxScore = max(self.redScore, self.blueScore)

            self.totalAmpNotes = self.autoAmpNotes + self.teleAmpNotes
            self.totalSpeakerNotes = self.autoSpeakerNotes + self.teleSpeakerNotes
            self.totalNotes = (
                self.totalAmpNotes + self.totalSpeakerNotes + self.trapNotes
            )

            # self.ensembleRP = 0
            # if red["ensembleBonusAchieved"]:
            #     self.ensembleRP = self.ensembleRP + 1
            # if blue["ensembleBonusAchieved"]:
            #     self.ensembleRP = self.ensembleRP + 1

            # self.melodyRP = 0
            # if red["melodyBonusAchieved"]:
            #     self.melodyRP = self.melodyRP + 1
            # if blue["melodyBonusAchieved"]:
            #     self.melodyRP = self.melodyRP + 1

            self.totalRP = red["rp"] + blue["rp"]

            # self.coop = 0
            # if red['coopNotePlayed']:
            #     self.coop = self.coop + 1o
            # if blue['coopNotePlayed']:
            #     self.coop = self.coop + 1

        else:
            self.autoAmpNotes = 0
            self.autoSpeakerNotes = 0
            self.teleAmpNotes = 0
            self.teleSpeakerNotes = 0
            self.trapNotes = 0
            self.amplifiedSpeakerNotes = 0
            self.numberOfSpotlights = 0
            self.redScore = 0
            self.blueScore = 0
            self.maxScore = 0
            self.totalAmpNotes = 0
            self.totalSpeakerNotes = 0
            self.totalNotes = 0
        if self.zebraData is not None:
            self.computeDistance()

    def computeDistance(self):
        if self.zebraData is not None:
            self.totalDistanceTraveled = 0

            team1Zebra = self.zebraData.alliances.blue[0]
            team2Zebra = self.zebraData.alliances.blue[1]
            team3Zebra = self.zebraData.alliances.blue[2]
            team4Zebra = self.zebraData.alliances.red[0]
            team5Zebra = self.zebraData.alliances.red[1]
            team6Zebra = self.zebraData.alliances.red[2]

            self.totalDistanceTraveled = (
                getTeamDistance(team1Zebra)
                + getTeamDistance(team2Zebra)
                + getTeamDistance(team3Zebra)
                + getTeamDistance(team4Zebra)
                + getTeamDistance(team5Zebra)
                + getTeamDistance(team6Zebra)
            )
        else:
            self.totalDistanceTraveled = 0
