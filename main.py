from flask import Flask, render_template
from flask import request
# import time
import random
import schedule
import threading
from flask import Flask, render_template, send_file
from flask import request
from nexusData import nexusData
from statbotData import getTeam
from tbaPulseData import getRankings, getPrediction
from triva import getQuestion

from HensightStatsManager import HensightStatsManager
from SlideHTMLGenerators import *
from TBAData import TBAData

listindex = 0
old = ''
old2 = ''
old3 = ''
app = Flask(__name__)

TBAData = TBAData()

# TBAData.load_events("data.txt")
#
#
TBAData.update_current_event_data("data.txt")
TBAData.load_from_file("data.txt")

# #
hensightStats = HensightStatsManager(TBAData)
hensightStats.update_stats()
#
def update_this_event():
    print("---updating---")
    TBAData.update_current_event_data("data.txt")
    print("---update finished---")

# schedule.every(3).minutes.do(update_this_event)

def loop():
    # print("-fnc run-")
    while True:
        # print("-loop run-")
        schedule.run_pending()
        time.sleep(1)
b = threading.Thread(name='loop', target=loop)
b.start()

def make_graph() -> list[str]:

    listofresults = [
                        eggs_in_match(toggle_list[1]), feather_message(toggle_list[2]), chicken_notes(toggle_list[3]),
                        chicken_weight(toggle_list[4]), eggs_in_season(toggle_list[5], True), robo_name(toggle_list[6]),
                        chicken_noise(toggle_list[7]), chicken_eat(toggle_list[8]), chicken_cycles(toggle_list[9]),
                        battery(toggle_list[10]), event_total_notes(toggle_list[11], event_toggle),
                        event_trap_notes(toggle_list[12], event_toggle), event_high_score(toggle_list[13], event_toggle), spotlight_percent(toggle_list[14], event_toggle),
                        global_total_notes(toggle_list[15]), global_high_score(toggle_list[16]), event_speaker_notes(toggle_list[17], event_toggle),
                        global_amp_notes(toggle_list[18]), event_travel(toggle_list[19], event_toggle), global_travel(toggle_list[20]), event_alliance_score(toggle_list[21], event_toggle),
                        # global_amplified_speaker(toggle_list[22]), compare_auto_notes(toggle_list[23], event_toggle), melody_rp(toggle_list[24])
                     ]
    reallist = []
    for result in listofresults:
        if result != "bad":
            reallist.append(result)
    return reallist

event_toggle = True
toggle_list = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, True, True, True]


@app.route("/")
def index():
    return render_template('hensight.html')

@app.route('/pulse_rip_off')
def pulseRipOff():
    return render_template('pulsemain.html')
@app.route('/pulse_schedule')
def pulseSchedule():
    return render_template('pulse_schedule.html')
@app.route('/pulse_ranking')
def pulseRanking():
    return render_template('pulse_ranking.html')

@app.route("/getnexusdata")
def getNextMatch():
    return nexusData()
@app.route("/getstatbotdata")
def getStatBotData():
    return getTeam()
@app.route("/getranking")
def getRanking():
    return getRankings()
@app.route("/getprediction")
def prediction():
    return getPrediction()


@app.route("/autos")
def autos():
    return render_template('autos.html')
@app.route("/autos2")
def autos2():
    return render_template('autos2.html')
@app.route("/autos3")
def autos3():
    return render_template('autos3.html')


@app.route("/cad")
def func():
    return render_template('cad.html')


@app.route("/common.js")
def commonjs():
    return send_file("./templates/common.js")
@app.route("/style.css")
def stylecss():
    return send_file("./templates/style.css")
@app.route('/AmpLane.json')
def amplane():
    return send_file("./static/AmpLanePADEF.traj")
@app.route('/SourceLane.json')
def sourcelane():
    return send_file("./static/SourceLanePHGF.traj")
@app.route('/CenterLane.json')
def centerlane():
    return send_file("./static/CenterLanePDEABC.traj")
@app.route('/FriedEgg.glb')
def serve_obj_file():
    return send_file("./static/FriedEgg.glb")

@app.route('/FieldCadSmall')
def serve_small_file():
    return send_file("./static/CrescendoFieldSmall.gltf")

@app.route('/OrbitControls.js')
def serve_obje_file():
    return send_file("./OrbitControls.js")

@app.route('/reveal')
def reveal():
    return render_template('reveal.html')

@app.route('/request')
def main():
    global listindex
    global old
    global old2
    global old3
    html = make_graph()
    if old == chicken_notes(True):
        # print('\n\nchoice:',chicken_foul(),'\nold:',old,'\nold2:',old2,'old3:',old3,'\n\n')
        old3 = old2
        old2 = old
        old = chicken_foul()
        return chicken_foul()
    choice = random.choice(html)
    if choice != old and choice != old2 and choice != old3:
        # print('\n\nchoice:',choice,'\nold:',old,'\nold2:',old2,'\nold3:',old3,'\n\n')
        old3 = old2
        old2 = old
        old = choice
        return choice
    else:
        return main()
    # if len(html)-1 > listindex:
    #     listindex +=1
    # else:
    #     listindex = 0
    # return html[listindex]

@app.route('/jsonrequest')
def jsonRequest():
    return [main()]

@app.route('/goback')
def goback():
    old = old2
    old2 = old3
    old3 = easter_egg()
    return old
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/fet', methods=['POST'])
def dashrequest():
    global toggle_list
    toggle_list = request.json
    return "hi"


@app.route('/testhtml')
def test_html():
    return render_template('test.html')


@app.route('/spin')
def CHICKEN_SPIN():
    return render_template('chickenspin.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')
@app.route('/menu/robot')
def robo():
    return render_template('robomenu.html')
@app.route('/menu/misc')
def misc():
    return render_template('misc.html')
@app.route('/menu/soon')
def soon():
    return render_template('comming_soon.html')
@app.route('/menu/games')
def games():
    return render_template('games.html')
@app.route('/crossy')
def crossy():
    return render_template('crossy.html')


@app.route('/triva')
def triva():
    return render_template('triva.html')
@app.route('/getqna')
def getQNA():
    return getQuestion()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
    print("hi")