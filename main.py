import os
import sys
import psycopg2
import plotly.graph_objects as go
from flask import Flask, render_template
import operator
from flask import Request
listindex = 0
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
except psycopg2.OperationalError:
    print(f"Unable to connect to database. Are you SSHed? Error: {sys.exc_info()[0]}")
    quit(0)

# Create a cursor
cur = conn.cursor()

postgresSQL_team_Query = 'SELECT team_key FROM "Teams"'
cur.execute(postgresSQL_team_Query)
teams = cur.fetchall()

#returns [percent acc of our team for amp in tele, percent acc of average of all other teams for amp in tele]
def get_amp_acc() -> list[float]:
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
def get_speaker_acc() -> list[float]:
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
def get_auto_acc() -> list[float]:
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
#returns number of traps scored for our team
def get_trap_number() -> str:
    postgresSQL_1540_trap_Query = f"""SELECT trap_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_trap_Query)
    trapnumber = cur.fetchall()
    total = 0
    trapnumber = round(total / len(trapnumber), 2)
    if trapnumber > 0:
        return trapnumber
#returns True or False for wether or not our robot has broke
def get_broke() -> bool:
    postgresSQL_broke_Query = """SELECT is_broke FROM "TeamMatches" WHERE team_key='1540' AND is_broke='True'"""
    cur.execute(postgresSQL_broke_Query)
    broke = cur.fetchall()
    if broke == []:
        return False
    else:
        return True

@app.route("/")
def index():
    return render_template('hensight.html')
def get_trap_graph():
        if get_trap_number() != None:
            return "<h4> We have scored in the trap</h4><h3>"+ str(get_trap_number()) +"</h3> times</h4>"
        else:
            return "bad"
def get_amp_graph():
        # if get_amp_acc()[0] >= 0.90 and get_amp_acc()[0] > get_amp_acc()[1]:
                ampfig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_amp_acc(), marker_color="rgb(255, 193, 69)"))
                ampfig.update_layout(plot_bgcolor='rgb(28, 28, 28)')
                ampfig.update_layout(paper_bgcolor='rgb(28, 28, 28)')
                ampfig.update_layout(font=dict(color="white", size=14, family = "Poppins"))
                ampfig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                ampfig.update_xaxes(title_text="Amp Accuracy", title_font=dict(color="white", family="Poppins"))
                amp_html = ampfig.to_html (
                    include_plotlyjs=True, 
                    full_html=False,
                    
                )
                return amp_html
        # else:
        #     return bad
def get_speaker_graph():
        # if get_speaker_acc()[0] >= 0.90 and get_speaker_acc()[0] > get_speaker_acc()[1]:
            speakerfig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_speaker_acc(), marker_color="rgb(255, 193, 69)"))
            speakerfig.update_layout(plot_bgcolor='rgb(28, 28, 28)')
            speakerfig.update_layout(paper_bgcolor='rgb(28, 28, 28)')
            speakerfig.update_layout(font=dict(color="white", size=14, family = "Poppins"))
            speakerfig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            speakerfig.update_xaxes(title_text="Speaker Accuracy", title_font=dict(color="white", family="Poppins"))
            speaker_html = speakerfig.to_html(
                include_plotlyjs=True,
                full_html=False,
            )
            return speaker_html
        # else:
            # return "bad"
def auto_acc_graph():
        # if get_auto_acc()[0] >= 0.70 and get_auto_acc()[0] > get_auto_acc()[1]:
            autofig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_auto_acc(), marker_color="rgb(255, 193, 69)"))
            autofig.update_layout(plot_bgcolor='rgb(28, 28, 28)')
            autofig.update_layout(paper_bgcolor='rgb(28, 28, 28)')
            autofig.update_layout(font=dict(color="white", size=14, family = "Poppins"))
            autofig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            autofig.update_xaxes(title_text="Auto Accuracy", title_font=dict(color="white", family="Poppins"))
            auto_html = autofig.to_html(
                include_plotlyjs=True,
                full_html=False,
            )
            return auto_html
        # else:
        #     return "bad"
def get_broke_graph():
        if get_broke() == False:
            return "<h4>Team 1540's robot has broken</h4><h3>0<h3><h4> times this competition</h4>"
        else:
            return "bad"
def make_graph() -> str:


    listofresults=[get_trap_graph(), get_amp_graph(), get_speaker_graph(), auto_acc_graph(), get_broke_graph()]
    reallist = []
    for result in listofresults:
        if result != "bad":
            reallist.append(result)
    return reallist

@app.route('/request')
def main():
    global listindex
    html = make_graph()
    if len(html)-1 != listindex:
        listindex = listindex + 1
    else:
        listindex = 0
    return html[listindex]

@app.route('/gitfeet')
def gitfeet():
    return '<marquee><h4 style="font-size: 30px">GIT FEET</h4><h4 style="font-size: 30px">GIT FEEt</h4><h4 style="font-size: 30px">GIT FEET</h4><h4 style="font-size: 30px">GIT FEEt</h4><h4 style="font-size: 30px">GIT FEET</h4></marquee>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)

