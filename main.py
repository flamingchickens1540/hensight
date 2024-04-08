from flask import Flask, render_template
from flask import request
import time
import random

from flask import Flask, render_template, send_file
from flask import request


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
TBAData.load_from_file("data.txt")
# TBAData.update_current_event_data("SaturdayTest.txt")
# #
hensightStats = HensightStatsManager(TBAData)
hensightStats.update_stats()
#





def make_graph() -> list[str]:
    listofresults = [
                        eggs_in_match(toggle_list[1]), feather_message(toggle_list[2]), chicken_notes(toggle_list[3]),
                        chicken_weight(toggle_list[4]), eggs_in_season(toggle_list[5], True), robo_name(toggle_list[6]),
                        chicken_noise(toggle_list[7]), chicken_eat(toggle_list[8]), chicken_cycles(toggle_list[9]),
                        battery(toggle_list[10]), logodvd(toggle_list[11]), event_total_notes(toggle_list[12]), 
                        event_trap_notes(toggle_list[13]), event_high_score(toggle_list[14]), spotlight_percent(toggle_list[15]),
                        global_total_notes(toggle_list[16])
                     ]
    reallist = []
    for result in listofresults:
        if result != "bad":
            reallist.append(result)
    return reallist


toggle_list = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]


@app.route("/")
def index():
    return render_template('hensight.html')


@app.route("/cad")
def func():
    return render_template('cad.html')


@app.route('/FriedEgg.glb')
def serve_obj_file():
    return send_file("./static/FriedEgg.glb")


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
        if old != thank_msg(True) and old2 != thank_msg(True) and old3 != thank_msg(True):
            # print('\n\nchoice:',thank_msg(True),'\nold:',old,'\nold2:',old2,'old3:',old3,'\n\n')
            old3 = old2
            old2 = old
            old = thank_msg(True)
            return thank_msg(True)
        else:
            # print('\n\nchoice:',robo_name(True),'\nold:',old,'\nold2:',old2,'old3:',old3,'\n\n')
            old3 = old2
            old2 = old
            old = logodvd(True)
            return logodvd(True)
    # if len(html)-1 > listindex:
    #     listindex +=1
    # else:
    #     listindex = 0
    # return html[listindex]

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
    print("hi")