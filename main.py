import random, os, TBAData, HensightStatsManager
from flask import Flask, render_template, send_file
from flask import request
from nexusData import getNexusData
# from statbotData import getTeam
from tbaPulseData import getRankings, getPrediction, getMatchSchedule
# from triva import getQuestion
from SlideHTMLGenerators import *
from dotenv import load_dotenv


listindex = -1
old, old2, old3 = "", "", ""
app = Flask(__name__)

load_dotenv()
photos = os.getenv("photos")
year = os.getenv("year")

# TBAData.load_events(year=year, genKeys=False, writeKeys=True, shouldProgress=False)
HensightStatsManager.update_stats()

toggles = {
        "eggs_in_season": True,
        "eggs_in_match": True,
        "thank_msg": True,
        "feather_msg": True,
        "chicken_notes": True,
        "chicken_weights": True,
        "chicken_eat": True,
        "battery": True,
        "logodvd": False,
        "trex": True,
        "chicken_count": True,
        "chicken_eye": True,
        "chicken_breed": True,
        "egg_time": True,
        "egg_pore": True,
        "points_scored": True,
        "average_points_permach": True,
        "penalty_points": True,
        "auto_points": True,
        "percent_last_year": True,
        "matches_played": True
    }
    
listOfResuts = [
        eggs_in_season(toggles["eggs_in_season"]),
        eggs_in_match(toggles["eggs_in_match"]),
        thank_msg(toggles["thank_msg"]),
        feather_message(toggles["feather_msg"]),
        chicken_notes(toggles["chicken_notes"]),
        chicken_foul(toggles["chicken_notes"]),
        chicken_weight(toggles["chicken_weights"]),
        chicken_eat(toggles["chicken_eat"]),
        battery(toggles["battery"]),
        logodvd(toggles["logodvd"]),
        trex(toggles["trex"]),
        chicken_count(toggles["chicken_count"]),
        egg_time(toggles["egg_time"]),
        egg_pore(toggles["egg_pore"]),
        points_scored(toggles["points_scored"]),
        average_points_permatch(toggles["average_points_permach"]),
        penalty_points(toggles["penalty_points"]),
        auto_poitns(toggles["auto_points"]),
        percent_last_year(toggles["percent_last_year"]),
        matches_played(toggles["matches_played"])
    ]

random.shuffle(listOfResuts)

def make_graph():
    realList = []
    for i in listOfResuts:
        if i != "bad":
            realList.append(i)
    return realList

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/hensight")
def index():
    return render_template("hensight.html")


@app.route("/pulse_rip_off")
def pulseRipOff():
    return render_template("pulsemain.html")


@app.route("/pulse_schedule")
def pulseSchedule():
    return render_template("pulse_schedule.html")


@app.route("/pulse_ranking")
def pulseRanking():
    return render_template("pulse_ranking.html")

@app.route("/drive-team")
def driveTeam():
    return render_template("drive_team.html")

driveTeamData = ""

@app.route("/post-drive-team", methods=["POST"])
def postDriveTeam():
    global driveTeamData
    driveTeamData = request.json
    return "hi"

@app.route("/get-drive-team")
def getDriveTeam():
    global driveTeamData
    json = {"msg": driveTeamData}
    driveTeamData = ""
    return json

@app.route("/tbadata")
def tbadata():
    return getMatchSchedule()

@app.route("/getnexusdata")
def getNextMatch():
    return getNexusData()


# @app.route("/getstatbotdata")
# def getStatBotData():
#     return getTeam()


@app.route("/getranking")
def getRanking():
    return getRankings()


@app.route("/getprediction")
def prediction():
    return getPrediction()


@app.route("/autos")
def autos():
    return render_template("autos.html")


@app.route("/autos2")
def autos2():
    return render_template("autos2.html")


@app.route("/autos3")
def autos3():
    return render_template("autos3.html")


@app.route("/cad")
def func():
    return render_template("cad.html")


@app.route("/common.js")
def commonjs():
    return send_file("./templates/common.js")


@app.route("/style.css")
def stylecss():
    return send_file("./templates/style.css")


@app.route("/AmpLane.json")
def amplane():
    return send_file("./static/AmpLanePADEF.traj")


@app.route("/SourceLane.json")
def sourcelane():
    return send_file("./static/SourceLanePHGF.traj")


@app.route("/CenterLane.json")
def centerlane():
    return send_file("./static/CenterLanePDEABC.traj")


@app.route("/FriedEgg.glb")
def serve_obj_file():
    return send_file("./static/FriedEgg.glb")


@app.route("/FieldCadSmall")
def serve_small_file():
    return send_file("./static/CrescendoFieldSmall.gltf")


@app.route("/OrbitControls.js")
def serve_obje_file():
    return send_file("./OrbitControls.js")


@app.route("/reveal")
def reveal():
    return render_template("reveal.html")


@app.route("/request")
def main():
    global listindex
    # global old
    # global old2
    # global old3
    html = make_graph()
    # if old == chicken_notes(True):
    #     # print('\n\nchoice:',chicken_foul(),'\nold:',old,'\nold2:',old2,'old3:',old3,'\n\n')
    #     old3 = old2
    #     old2 = old
    #     old = chicken_foul()
    #     return chicken_foul()
    # choice = random.choice(html)
    # if choice != old and choice != old2 and choice != old3:
    #     # print('\n\nchoice:',choice,'\nold:',old,'\nold2:',old2,'\nold3:',old3,'\n\n')
    #     old3 = old2
    #     old2 = old
    #     old = choice
    #     return choice
    # else:
    #     return main()
    if len(html)-1 > listindex:
        listindex +=1
    else:
        listindex = 0
    return html[listindex]


@app.route("/jsonrequest")
def jsonRequest():
    return [main()]


@app.route("/goback")
def goback():
    old = old2
    old2 = old3
    old3 = easter_egg()
    return old


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/fet", methods=["POST"])
def dashrequest():
    global toggle_list
    toggle_list = request.json
    return "hi"


@app.route("/testhtml")
def test_html():
    return render_template("test.html")


@app.route("/spin")
def CHICKEN_SPIN():
    return render_template("chickenspin.html")

@app.route("/gallery")
def gallery():
    random.shuffle(photos)
    return render_template("gallery.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/menu/robot")
def robo():
    return render_template("robomenu.html")


@app.route("/menu/misc")
def misc():
    return render_template("misc.html")


@app.route("/menu/soon")
def soon():
    return render_template("comming_soon.html")


@app.route("/menu/games")
def games():
    return render_template("games.html")


@app.route("/crossy")
def crossy():
    return render_template("crossy.html")

@app.route("/getphoto")
def photo():
    return photos




@app.route('/triva')
def triva():
    return render_template('triva.html')
@app.route('/getqna')
def getQNA():
    return getQuestion()


@app.route("/meanmachine")
def meanmachine():
    return render_template('meanmachine.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
    print("hi")
