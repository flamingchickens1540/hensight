# import psycopg2
# import plotly.graph_objects as go
from flask import Flask, render_template
from flask import request
import time
import random
from flask import Flask, render_template, send_file
listindex = 0
old = ''
old2 = ''
old3 = ''
app = Flask(__name__)
# #------------------------------------------------------------------------------------------------------------#

# comp = "2024orsal"

# #------------------------------------------------------------------------------------------------------------#

# # Define the connection parameters
# host = os.getenv("DB_HOST", default="127.0.0.1")
# port = int(os.getenv("DB_PORT", default=5432))
# database = os.getenv("DB_NAME", default="crescendo_scouting")
# user = os.getenv("DB_USER", default="chargedup_scouting_analysis")
# password = os.getenv("DB_PASSWORD", default="amptrapspeaker1540")

# # Connect to the database
# try:
#     conn = psycopg2.connect(
#         host=host,
#         port=port,
#         database=database,
#         user=user,
#         password=password,
#     )
# except psycopg2.OperationalError:
#     print(f"Unable to connect to database. Are you SSHed? Error: {sys.exc_info()[0]}")
#     quit(0)

# # Create a cursor
# cur = conn.cursor()

# postgresSQL_team_Query = 'SELECT team_key FROM "Teams"'
# cur.execute(postgresSQL_team_Query)
# teams = cur.fetchall()


# def sum_auto_amp_sec():
#     total = 0
#     for team in teams:
#         postgresSQL_auto_amp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_amp_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#         else: return 0
#     return total
# def avg_auto_amp_sec():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_auto_amp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_amp_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_auto_amp_miss():
#     total = 0
#     for team in teams:
#         postgresSQL_auto_amp_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_amp_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_auto_amp_miss():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_auto_amp_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_amp_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_tele_amp_sec():
#     total = 0
#     for team in teams:
#         postgresSQL_tele_amp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_amp_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_tele_amp_sec():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_tele_amp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_amp_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total * 100

# def sum_tele_amp_miss():
#     total = 0
#     for team in teams:
#         postgresSQL_tele_amp_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_amp_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_tele_amp_miss():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_tele_amp_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_amp_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_auto_speaker_sec():
#     total = 0
#     for team in teams:
#         postgresSQL_auto_speaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_speaker_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_auto_speaker_sec():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_auto_speaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_speaker_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_tele_speaker_sec():
#     total = 0
#     for team in teams:
#         postgresSQL_tele_speaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_speaker_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_tele_speaker_sec():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_tele_speaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_speaker_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_auto_speaker_miss():
#     total = 0
#     for team in teams:
#         postgresSQL_auto_speaker_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_speaker_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_auto_speaker_miss():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_auto_speaker_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_auto_speaker_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total

# def sum_tele_speaker_miss():
#     total = 0
#     for team in teams:
#         postgresSQL_tele_speaker_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_speaker_Query)
#         if cur.rowcount != 0:
#             data = cur.fetchall()
#             for i in data:
#                 total += i[0]
#     return total
# def avg_tele_speaker_miss():
#     big_total = 0
#     len_total = 0
#     for team in teams:
#         postgresSQL_tele_speaker_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
#         cur.execute(postgresSQL_tele_speaker_Query)
#         if cur.rowcount !=0:
#             data = cur.fetchall()
#             for i in data:
#                 big_total += i[0]
#             len_total += len(data)
#     total = round(big_total / len_total, 2)
#     return total



def thank_msg(toggle):
    if toggle:
        return '<h4>Team 1540 Thanks</h4><h3>YOU</h3><h4>for joining us in our pits!</h4>'
    else: return 'bad'
def eggs_in_match(toggle):
    if toggle:
        return "<h4>During each match over</h4><h3>520,000</h3><h4>eggs are laid in the US!</h4>"
    else: return 'bad'
def feather_message(toggle):
    if toggle:
        return "<h4>There are as many people that do FIRST as feathers on </h4><h2>Ten and Half chickens!</h2>"  
    else: return 'bad'
def chicken_notes(toggle):
    if toggle: return "<h4 style='display:inline-block;'>A chicken of the </h4><p style='display:inline-block;'></p><h4 style='color: #FFC145; display:inline-block;'> non-flaming</h4><h4>variety is expected to score</h4><h3>0</h3><h4>notes during a match!</h4>"
    else: return 'bad'
def chicken_weight(toggle):
    if toggle: return '<h4>The heaviest chicken was 22lbs! That is</h4><h3>88 lbs</h3><h4>less than the weight of our robot!</h4>'
    else: return 'bad'
def eggs_in_season(toggle, html):
    if toggle:
        current_time = round(time.time())
        secconds_passed = round(current_time - 	1704571200)
        years = secconds_passed / 31536000
        eggs_laied = round(years * 250)
        if html:
            return f'<h4>A single chicken would have laid</h4><h3>{eggs_laied}</h3><h4>eggs since build season started</h4>'
        else: return eggs_laied
    else: return 'bad'
def robo_name(toggle):
    if toggle: return "<h4>Our robot is named Fried Egg because</h4><h2>We're cooking</h2><h4>this year!</h4>"
    else: return 'bad'
# def event_scored(toggle, html):
#     if toggle:
#         amp_total = sum_auto_amp_sec() + sum_tele_amp_sec()
#         speaker_total = sum_auto_speaker_sec() + sum_tele_speaker_sec()
#         big_total = amp_total + speaker_total
#         number = ('{:,}'.format(big_total)) 
#         if html: return f'<h4>There has been</h4><h3>{number}</h3><h4>notes scored this event!</h4>'
#         else: return big_total
#     else: return 'bad'
# def event_acc(toggle, html):
#     if toggle:
#         scored = event_scored(True, False)
#         miss_amp = sum_auto_amp_miss() + sum_tele_amp_miss()
#         miss_speaker = sum_auto_speaker_miss() + sum_tele_speaker_miss()
#         missed = miss_speaker + miss_amp
#         shots = scored + missed
#         acc = round(scored / missed, 3)
#         if html: return f'<h4>Teams at this event have scored</h4><h3>{acc * 100}%</h3><h4>of total notes shot!</h4>'
#     else: return 'bad'
def chicken_foul():
    return "<h1>However, in the whimsical scenario where we decide to replace the robot on the field with a live chicken, a cascade of unforeseen consequences would likely unfold. Picture this: amidst the high-stakes game, the unsuspecting chicken, blissfully unaware of the intricate rules governing the match, would likely become the unwitting perpetrator of an array of tech fouls. The referee, undoubtedly perplexed by the surreal turn of events, might find themselves compelled to brandish a red card, signaling not only an expulsion from the game but also drawing attention to the peculiar nature of the infringement.</h1>"
def chicken_noise(toggle):
    if toggle: return "<h4>Chickens can squawk as loud as</h4><h2>70 decibels<h2><h4>about as loud as the average classroom</h4>"
    else: return 'bad'
def chicken_eat(toggle):
    if toggle: return '<h4>FRC Students eat approximately</h4><h3 style="font-size: 17rem;">7,917,000</h3><h4>chickens per year</h4>'
    else: return 'bad'
def chicken_cycles(toggle):
    if toggle:
        return '<h4 style="display:inline-block;">A chicken of the </h4><p style="display:inline-block;"> </p><h4 style="display:inline-block; color: #FFC145;"> non-flaming</h4><h4>variety can make a speaker cycle in</h4><h2>3 seconds!</h2>'
    else: return 'bad'
def socials(toggle):
    if toggle: return '<h5>A chicken running on a hamster wheel would take</h5><h3>5 hours</h3><h5>to generate enough power for a ES 17-12 battery</h5>'
    else: return 'bad'
def logodvd(toggle):
    if toggle: return '<marquee class="marquee" behavior="alternate" direction="down"scrollamount="20"><marquee behavior="alternate" width="100%" scrollamount="20"><img width="250px" src="https://avatars.githubusercontent.com/u/5280254?s=200&v=4" alt="dvd" id="spin"></marquee></marquee>'
    else: return 'bad'

def make_graph() -> list[str]:
    listofresults=[eggs_in_match(toggle_list[1]), feather_message(toggle_list[2]), chicken_notes(toggle_list[3]), chicken_weight(toggle_list[4]), eggs_in_season(toggle_list[5], True), robo_name(toggle_list[6]), chicken_noise(toggle_list[7]), chicken_eat(toggle_list[8]), chicken_cycles(toggle_list[9]), socials(toggle_list[10]), logodvd(toggle_list)]
    reallist = []
    for result in listofresults:
        if result != "bad":
            reallist.append(result)
    return reallist
toggle_list = [True, True, True, True, True, True, True, True, True, True, True, True, True]
@app.route("/")
def index():
    return render_template('hensight.html')
@app.route("/cad")
def func():
    return render_template('cad.html')
@app.route("/reveal")
def fun():
    return render_template('reveal.html')
@app.route('/FriedEgg.glb')
def serve_obj_file():
        return send_file("./static/FriedEgg.glb")
@app.route('/OrbitControls.js')
def serve_obje_file():
        return send_file("./OrbitControls.js")
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
            old = robo_name(True)
            return robo_name(True)
    # if len(html)-1 > listindex:
    #     listindex +=1
    # else:
    #     listindex = 0
    # return html[listindex]

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/fet', methods = ['POST'])
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
    app.run(host='0.0.0.0',port=5001,debug=True)