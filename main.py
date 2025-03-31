import os
os.chdir('/home/projects/Hensight/hensight')
# print("current working dir: ", os.getcwd())

import random, TBAData, HensightStatsManager, vars, requests
from flask import Flask, render_template, send_file
from flask import request
from nexusData import getNexusData
# from statbotData import getTeam
from tbaPulseData import getRankings, getPrediction, getMatchSchedule
# from triva import getQuestion
from SlideHTMLGenerators import *
from dotenv import load_dotenv

listindex = -1
old = ""
app = Flask(__name__)

load_dotenv()
year = vars.year
photos = ['https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/afdfd7cd-a29b-4ef5-be49-52d8101fd1e3/StormSurge24-3667.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/a83998d3-0f39-4e12-adad-b0b559a9777b/StormSurge24-00774.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/3368d204-7f0a-4add-9907-cc3a393372f8/StormSurge24-3737.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/3dcd5a00-e684-4032-8640-7cec2fffcefc/StormSurge24-3666.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/467ab25e-883e-4176-a6b2-1c23d4f619aa/StormSurge24-3696.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/379ab063-c53d-41ba-9eef-5db12e663c60/StormSurge24-3704.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/e64bbab9-6f57-4507-855f-f744ae34b42e/StormSurge24-3664.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/5e3175f3-7eec-4aa2-9d96-18a747c72bfd/IMG_2601.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/9b408ba5-adea-4fd0-9535-a10ac67b828b/IMG_3071.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/cb1235d7-1096-4470-8331-555e944f914c/IMG_2702.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/19e6280e-8c81-4371-9cc3-6f4b668edfaa/IMG_3059.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/8bc93c80-9655-4488-9daf-fea609a1a1c9/IMG_2216.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/9a88f895-920a-4870-8a01-32de3a238d0d/IMG_2333.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/cb397f23-e796-4ca0-a7ac-5e4adee142e9/IMG_2318.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/1bb24602-5cca-4442-a27e-3ab2c9a3a15f/IMG_2359.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/55fe61a7-4244-4993-83a1-c0da87ecfc9f/IMG_2355.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/3a3a5fb3-ca8b-41af-92fd-51d9f93f13d5/IMG_2383.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/526cf8c3-d3d7-41fd-b6f8-c599180f3d41/IMG_2471.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/599bf7e8-1516-4c65-85c4-11e422788edb/IMG_2529.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/eddd0f71-f780-41d1-aa1a-d655a046b8ea/IMG_0071.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/d3c12083-ed31-4122-9a9d-61a3fac80a2e/DSC_6004.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/2a7ee077-dda5-4260-b351-18d0b0247cc0/DSC_5996.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/ba6ab153-c6ad-48a1-8db4-8994a7635b88/DSC_5979.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/fb180b62-da35-40ff-8bb7-d54a0a43424b/DSC_5470.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/d4eb9a7e-c933-4b28-b6e3-16b9e29485e5/DSC_5723.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/24e9b334-e87c-4ef0-ba11-294a1ca72472/DSC_6227.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/3f9872b2-5641-4506-842e-c9fc240eae67/DSC_5978.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/b05f35dd-0c38-46d6-92ad-93ef31b3c3fe/DSC_6286.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/d19b5b04-abbf-406c-9ae6-82b0a77682f6/DSC_5871.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/8069cd26-6ea9-417e-8fa2-9ff29a056fe9/DSC_6294.jpg?format=1000w','https://images.squarespace-cdn.com/content/v1/634f81a61fae3d397cfce930/0de83fd5-1a12-40e8-96ae-dfac893d9483/DSC_6303.jpg?format=1000w']
channel = 'Match Stream'

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
        "logodvd": True,
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
        "percent_last_year": False, # off because no last year
        "matches_played": True,
        "chicken_face": True,
        "alliance_win_rate": True,
        "event_algae_processed": True,
        "event_rp_earned": True
    }
    
listOfResuts = [
        eggs_in_season(toggles["eggs_in_season"]),
        eggs_in_match(toggles["eggs_in_match"]),
        thank_msg(toggles["thank_msg"]),
        feather_message(toggles["feather_msg"]),
        chicken_notes(toggles["chicken_notes"]),
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
        matches_played(toggles["matches_played"]),
        chicken_face(toggles["chicken_face"]),
        alliance_win_rate(toggles["alliance_win_rate"]),
        event_algae_processed(toggles["event_algae_processed"]),
        event_rp_earned(toggles["event_rp_earned"])
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
    TBAData.update_this_event()
    return render_template("hensight.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

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

@app.route("/getchannel")
def getChannel():
    global channel
    return channel

@app.route("/updatechannel", methods=["POST"])
def updateChannel():
    global channel
    channel = request.json
    return "hi"


@app.route("/request")
def main():
    global listindex
    global old
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
    try: 
        if old == chicken_notes(True): 
            old = chicken_foul(True)
            return chicken_foul(True)
    except UnboundLocalError: print('err')
    if len(html)-1 > listindex:
        listindex +=1
    else:
        listindex = 0
    old = html[listindex]
    return html[listindex]


@app.route("/jsonrequest")
def jsonRequest():
    return [main()]


# @app.route("/goback")
# def goback():
#     old = old2
#     old2 = old3
#     old3 = easter_egg()
#     return old


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


@app.route("/judges")
def judges():
    return render_template("judges.html")

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

@app.route("/oapage")
def oapage():
    return render_template("oa.html")

@app.route("/webscrape")
def webscrape():
    response = requests.get("https://www.chiefdelphi.com/t/team-1540-flaming-chickens-2025-build-thread/476227")
    return response.text

@app.route("/getoa")
def oa():
    return [
        "<img src='https://lh7-rt.googleusercontent.com/docsz/AD_4nXf3F_NHJ0qSP1It-8yYHbzEGsbI6VaAiaZAIjmxPS-5A-w55QU-TfnogFk65S4ZJ5hRIKCpFFiDIgIeTeVtfnbEHzeaoHDkBFrhHUvhxnVO4HV9NmmTlf076nB0sHVU30OkIMkU3w?key=0mowtUxAPVVI1V24GVwCGe5F' alt = '' id='photo'></img>",
        '<iframe src="https://youtu.be/ys-cbw5E_xA" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="https://youtu.be/BcHkjhUNe_c" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="https://youtu.be/kce5nx2Hk1Y" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="https://youtu.be/a7XLVSBwA48" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="https://youtu.be/H98dzl4HpP0" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="" width="1366px" height="768px" frameborder="0"></iframe>',
        '<iframe src="" width="1366px" height="768px" frameborder="0"></iframe>',
    ]



@app.route('/triva')
def triva():
    return render_template('triva.html')
@app.route('/getqna')
# def getQNA():
#     return getQuestion()


@app.route("/meanmachine")
def meanmachine():
    return render_template('meanmachine.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
    print("hi")