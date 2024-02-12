import os
import sys
import psycopg2
import plotly.graph_objects as go
from flask import Flask
import operator

from charts import convert_to_html
from flask import Request

app = Flask(__name__)


# Define the connection parameters
host = os.getenv("DB_HOST", default="127.0.0.1")
port = int(os.getenv("DB_PORT", default=5432))
database = os.getenv("DB_NAME", default="crescendo_scouting")
user = os.getenv("DB_USER", default="chargedup_scouting_analysis")
password = os.getenv("DB_PASSWORD", default="amptrapspeaker1540")

# Connect to the database
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )
except:
    print(f"Unable to connect to database. Are you SSHed? Error: {sys.exc_info()[0]}")
    quit(0)

# Create a cursor
cur = conn.cursor()

postgresSQL_team_Query = 'SELECT team_key FROM "Teams"'
cur.execute(postgresSQL_team_Query)
teams = cur.fetchall()

#returns [percent acc of our team for amp in tele, percent acc of average of all other teams for amp in tele]
def get_amp_acc():
    for team in teams:
        postgresSQL_average_ampacc_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_ampacc_Query)
        sec_datapoints = cur.fetchall()   
        total = 0
        for datapoint in sec_datapoints:
            total += datapoint[0]
            sec_average_ampacc[team] = round(total / len(sec_datapoints), 2)
        total = 0
        for average in sec_average_ampacc:
            total += int(average[0])
        sec_final_average = round(total / len(sec_average_ampacc), 2)
    postgresSQL_1540_ampacc_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_ampacc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_ampacc_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_ampacc_Query)
        mis_datapoints = cur.fetchall()   
        total = 0
        for datapoint in mis_datapoints:
            total += datapoint[0]
            mis_average_ampacc[team] = round(total / len(mis_datapoints), 2)
        total = 0
        for average in mis_average_ampacc:
            total += int(average[0])
        mis_final_average = round(total / len(mis_average_ampacc), 2)
    postgresSQL_1540_ampacc_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_ampacc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    amp_acc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    amp_acc.append(round(sec_final_average / mis_final_average, 2))
    return amp_acc
sec_average_ampacc = {}
mis_average_ampacc = {}
amp_acc = []
#returns [percent acc of our team for speaker in tele, percent acc of average of all other teams for speaker in tele]
def get_speaker_acc():
    for team in teams:
        postgresSQL_average_speakeracc_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_speakeracc_Query)
        sec_datapoints = cur.fetchall()   
        total = 0
        for datapoint in sec_datapoints:
            total += datapoint[0]
            sec_average_speakeracc[team] = round(total / len(sec_datapoints), 2)
        total = 0
        for average in sec_average_speakeracc:
            total += int(average[0])
        sec_final_average = round(total / len(sec_average_speakeracc), 2)
    postgresSQL_1540_speakeracc_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_speakeracc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_speakeracc_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_speakeracc_Query)
        mis_datapoints = cur.fetchall()   
        total = 0
        for datapoint in mis_datapoints:
            total += datapoint[0]
            mis_average_speakeracc[team] = round(total / len(mis_datapoints), 2)
        total = 0
        for average in mis_average_speakeracc:
            total += int(average[0])
        mis_final_average = round(total / len(mis_average_speakeracc), 2)
    postgresSQL_1540_speakeracc_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_speakeracc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    speaker_acc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    speaker_acc.append(round(sec_final_average / mis_final_average, 2))
    return speaker_acc
sec_average_speakeracc = {}
mis_average_speakeracc = {}
speaker_acc = []
#returns [average of percent acc of amp in auto and percent acc of speaker in auto for our team, same thing for average of all other teams]
def get_auto_acc():
    for team in teams:
        postgresSQL_average_autospeakeracc_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_autospeakeracc_Query)
        sec_datapoints = cur.fetchall()   
        total = 0
        for datapoint in sec_datapoints:
            total += datapoint[0]
            sec_average_autospeakeracc[team] = round(total / len(sec_datapoints), 2)
        total = 0
        for average in sec_average_autospeakeracc:
            total += int(average[0])
        sec_final_average = round(total / len(sec_average_autospeakeracc), 2)
    postgresSQL_1540_autospeakeracc_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_autospeakeracc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_autospeakeracc_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_autospeakeracc_Query)
        mis_datapoints = cur.fetchall()   
        total = 0
        for datapoint in mis_datapoints:
            total += datapoint[0]
            mis_average_autospeakeracc[team] = round(total / len(mis_datapoints), 2)
        total = 0
        for average in mis_average_autospeakeracc:
            total += int(average[0])
        mis_final_average = round(total / len(mis_average_autospeakeracc), 2)
    postgresSQL_1540_autospeakeracc_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_autospeakeracc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    speakerautocalc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    speakerautocalc.append(round(sec_final_average / mis_final_average))



    for team in teams:
        postgresSQL_average_autoampacc_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_autoampacc_Query)
        sec_datapoints = cur.fetchall()   
        total = 0
        for datapoint in sec_datapoints:
            total += datapoint[0]
            sec_average_autoampacc[team] = round(total / len(sec_datapoints), 2)
        total = 0
        for average in sec_average_autoampacc:
            total += int(average[0])
        sec_final_average = round(total / len(sec_average_autoampacc), 2)
    postgresSQL_1540_autoampacc_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_autoampacc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_autoampacc_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
        cur.execute(postgresSQL_average_autoampacc_Query)
        mis_datapoints = cur.fetchall()   
        total = 0
        for datapoint in mis_datapoints:
            total += datapoint[0]
            mis_average_autoampacc[team] = round(total / len(mis_datapoints), 2)
        total = 0
        for average in mis_average_autoampacc:
            total += int(average[0])
        mis_final_average = round(total / len(mis_average_autoampacc), 2)
    postgresSQL_1540_autoampacc_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_autoampacc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    ampautocalc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    ampautocalc.append(round(sec_final_average / mis_final_average))
    autoacc.append(round(ampautocalc[0] / speakerautocalc[0], 2))
    autoacc.append(round(ampautocalc[1] / speakerautocalc[1], 2))
    return autoacc
sec_average_autospeakeracc = {}
mis_average_autospeakeracc = {}
sec_average_autoampacc = {}
mis_average_autoampacc = {}
ampautocalc = []
speakerautocalc = []
autoacc = []
#returns number of traps scored for our team, returns None if 0
def get_trap_number():
    postgresSQL_1540_trap_Query = f"""SELECT trap_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_trap_Query)
    trapnumber = cur.fetchall()
    total = 0
    trapnumber = round(total / len(trapnumber), 2)
    if trapnumber > 0:
        return trapnumber
#returns True or False for wether or not our robot has broke
def get_broke():
    postgresSQL_broke_Query = """SELECT is_broke FROM "TeamMatches" WHERE team_key='1540' AND is_broke='True'"""
    cur.execute(postgresSQL_broke_Query)
    broke = cur.fetchall()
    if broke == []:
        return False
    else:
        return True
    
print("Auto acc:",get_auto_acc())
print("Speaker acc:",get_speaker_acc())
print("Amp acc:", get_amp_acc())
print("has broke:", get_broke())
print("# of trap:", get_trap_number())


# Converting charts.py to html 

def get_chart(keys, values):

       x_data = [keys]
       y_data = [values]

       return convert_to_html(x_data=x_data, y_data=y_data)

html = get_chart()

frontend = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>HENSIGHT!!!!!!</title> <style> body { margin: 0; padding: 0; overflow: hidden; animation: fadein 1s forwards; /* Initial fade in */ } @keyframes fadeout { from { opacity: 1; /* Fully visible */ } to { opacity: 0; /* Fully transparent */ } } @keyframes fadein { from { opacity: 0; /* Fully transparent */ } to { opacity: 1; /* Fully visible */ } } </style> </head> <body> <div id="content"> </div> </body> <script> let faded = false var contents = ' + html + '; let currentSlide = 1; function showSlide() { for (var i = 0; i < contents.length; i++) { if (i + 1 == currentSlide) { document.getElementById("content").innerHTML = contents[i] } } if (currentSlide == contents.length) { currentSlide = 1 } else { currentSlide = (currentSlide + 1); } } setInterval(fadeEffect, 10000); setTimeout(function() { showSlide(); setInterval(showSlide, 10000); }, 1000); //chatgpt code plz do not touch plz if // Repeat the fade effect every 10 seconds (10000 ms) function fadeEffect() { console.log("fade started") document.body.style.animation = "fadeout 1s forwards"; // Fade out animation setTimeout(function() { document.body.style.animation = "fadein 1s forwards"; // Fade in animation }, 1000); // Wait for 2 seconds for fade out to complet } </script> </html> <style> h4 { font-size: 48px; } </style>'

@app.route('/')
def run():
    return frontend

# keys = [key[0] for key in list(descending_autoamps.keys())]
# values = [value for value in list(descending_autoamps.values())]

# fig.update_layout(
#     autosize=False,
#     width=1000,
#     height=1000,
#     margin=dict(l=50, r=50, b=100, t=100, pad=4),
#     paper_bgcolor="LightSteelBlue",
# )

# fig.show()


cur.close()
conn.close()

@app.route("/")
def hello_world():
    return "<p>Goodbye, World!</p>" 

# if __name__ == '__main__':
#     app.run(host='0.0.0',port=5001,debug=True)