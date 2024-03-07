import os
import sys
import psycopg2
import plotly.graph_objects as go
from flask import Flask, render_template
import operator
from flask import request
import time
listindex = 0
app = Flask(__name__)
#------------------------------------------------------------------------------------------------------------#

comp = "test"

#------------------------------------------------------------------------------------------------------------#

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
    sec_average_ampacc = {}
    mis_average_ampacc = {}
    amp_acc = []
    for team in teams:
        postgresSQL_average_ampacc_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_average_ampacc_Query)
        if cur.rowcount != 0:
            sec_datapoints = cur.fetchall()   
            total = 0
            for datapoint in sec_datapoints:
                total += datapoint[0]
                sec_average_ampacc[team] = round(total / len(sec_datapoints), 2)
            total = 0
            for average in sec_average_ampacc:
                total += int(average[0])
            sec_final_average = round(total / len(sec_average_ampacc), 2)
    postgresSQL_1540_ampacc_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_ampacc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_ampacc_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_ampacc_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_ampacc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    amp_acc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    amp_acc.append(round(sec_final_average / mis_final_average, 2))
    return amp_acc
#returns [percent acc of our team for speaker in tele, percent acc of average of all other teams for speaker in tele]
def get_speaker_acc() -> list[float]:
    sec_average_speakeracc = {}
    mis_average_speakeracc = {}
    speaker_acc = []
    for team in teams:
        postgresSQL_average_speakeracc_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_speakeracc_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_speakeracc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_speakeracc_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_speakeracc_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_speakeracc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    speaker_acc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    speaker_acc.append(round(sec_final_average / mis_final_average, 2))
    return speaker_acc
#returns [average of percent acc of amp in auto and percent acc of speaker in auto for our team, same thing for average of all other teams]
def get_auto_acc() -> list[float]:
    sec_average_autospeakeracc = {}
    mis_average_autospeakeracc = {}
    sec_average_autoampacc = {}
    mis_average_autoampacc = {}
    ampautocalc = []
    speakerautocalc = []
    autoacc = []
    for team in teams:
        postgresSQL_average_autospeakeracc_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_autospeakeracc_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_autospeakeracc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_autospeakeracc_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_autospeakeracc_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_autospeakeracc_Query)
    teamdata = cur.fetchall()
    total = 0
    for datapoint in teamdata:
        total += datapoint[0]
    mis_avgteamdata = round(total / len(teamdata), 2)
    speakerautocalc.append(round(sec_avgteamdata / mis_avgteamdata, 2))
    speakerautocalc.append(round(sec_final_average / mis_final_average))



    for team in teams:
        postgresSQL_average_autoampacc_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_autoampacc_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_autoampacc_Query)
    sec_teamdata = cur.fetchall()
    total = 0
    for datapoint in sec_teamdata:
        total += datapoint[0]
    sec_avgteamdata = round(total / len(sec_teamdata), 2)
    for team in teams:
        postgresSQL_average_autoampacc_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
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
    postgresSQL_1540_autoampacc_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
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
#returns number of traps scored for our team
def get_trap_number() -> str:
    postgresSQL_1540_trap_Query = f"""SELECT trap_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_trap_Query)
    trapnumber = cur.fetchall()
    total = 0
    trapnumberreal = round(total / len(trapnumber), 2)
    return trapnumberreal
#returns True or False for wether or not our robot has broke
def get_broke() -> bool:
    postgresSQL_broke_Query = f"""SELECT is_broke FROM "TeamMatches" WHERE team_key='1540' AND is_broke='True' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_broke_Query)
    broke = cur.fetchall()
    if broke == []:
        return False
    else:
        return True

def get_speaker_acc_noavg() -> list[float]:
    postgresSQL_1540_speaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_speaker_Query)
    missed1540 = cur.fetchall()
    total = 0
    for i in missed1540:
        total += i[0]
    if len(missed1540) != 0: missed1540avg = round(total / len(missed1540), 2)
    else: missed1540avg = 0
    postgresSQL_1540_speaker_Query2 = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_speaker_Query2)
    scored1540 = cur.fetchall()
    total = 0
    for i in scored1540:
        total += i[0]
    if len(scored1540) != 0: scored1540avg = round(total / len(scored1540), 2)
    else: scored1540avg = 0
    acc1540 = round(scored1540avg / missed1540avg , 2)
    acc_all = []
    for team in teams:
        postgresSQL_other_speaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_other_speaker_Query)
        missedother = cur.fetchall()
        total = 0
        for i in missedother:
            total += i[0]
        if len(missedother) != 0: missedotheravg = round(total / len(missedother), 2)
        else: missedotheravg = 0
        postgresSQL_other_speaker_Query2 = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_other_speaker_Query2)
        scoredother = cur.fetchall()
        total = 0
        for i in scoredother:
            total += i[0]
        if len(scoredother) != 0: scoredotheravg = round(total / len(scoredother), 2)
        else: scoredotheravg = 0
        acc_all.append(round(scoredotheravg / missedotheravg , 2))
    acc = [acc1540]
    for i in acc_all:
        acc.append(i)
    return acc
        
def get_amp_acc_noavg() -> list[float]:
    postgresSQL_1540_amp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
    cur.execute(postgresSQL_1540_amp_Query)
    missed1540 = cur.fetchall()
    if cur.rowcount != 0:
            total = 0
            for i in missed1540:
                total += i[0]
                missed1540avg = round(total / len(missed1540), 2)
            postgresSQL_1540_amp_Query2 = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
            cur.execute(postgresSQL_1540_amp_Query2)
            scored1540 = cur.fetchall()
            if cur.rowcount != 0:
                total = 0
                for i in scored1540:
                    total += i[0]
                    scored1540avg = round(total / len(missed1540), 2)
                acc1540 = round(scored1540avg / missed1540avg , 2)
                acc_all = []
                for team in teams:
                    postgresSQL_other_amp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
                    cur.execute(postgresSQL_other_amp_Query)
                    missedother = cur.fetchall()
                    if cur.rowcount != 0:
                        total = 0
                        for i in missedother:
                            total += i[0]
                            missedotheravg = round(total / len(missedother), 2)
                        postgresSQL_other_amp_Query2 = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
                        cur.execute(postgresSQL_other_amp_Query2)
                        scoredother = cur.fetchall()
                        if cur.rowcount != 0:
                            total = 0
                            for i in scoredother:
                                total += i[0]
                                scoredotheravg = round(total / len(missedother), 2)
                            acc_all.append(round(scoredotheravg / missedotheravg , 2))
                        acc = [acc1540]
                        for i in acc_all:
                            acc.append(i)
                        return acc


def get_trap_graph(toggle, html):
    if toggle:
        if html:
            if get_trap_number() > 0:
                return "<h4> We have scored in the trap</h4><h3>"+ str(get_trap_number()) +"</h3> times this event</h4>"
            else:
                return "bad"
        else: return get_trap_number()
    else: return "bad"

def get_speaker_comparison_keys():
    not_1540_speaker= []
    count = 0 

    for team in teams:
        if team == ('1540',):
            not_1540_speaker.append('1540')
        else:
            not_1540_speaker.append(f"{count}")
            count = count + 1

    speaker_comparison_raw_data = {}       
    count = 0

    for team in not_1540_speaker:
        speaker_acc_noavg = get_speaker_acc_noavg()
        speaker_comparison_raw_data[team] = speaker_acc_noavg[count]
        count = count + 1

    speaker_comparison_data = sorted(speaker_comparison_raw_data.items(), key=operator.itemgetter(1))
    speaker_comparison_data = dict(sorted(speaker_comparison_raw_data.items(), key=operator.itemgetter(1), reverse=True))

    speaker_comparison_keys = [key for key in list(speaker_comparison_data.keys())]
    speaker_comparison_values = [value for value in list(speaker_comparison_data.values())]

    return speaker_comparison_keys

def get_speaker_comparison_values():
    not_1540_speaker= []
    count = 0 

    for team in teams:
        if team == ('1540',):
            not_1540_speaker.append('1540')
        else:
            not_1540_speaker.append(f"{count}")
            count = count + 1

    speaker_comparison_raw_data = {}       
    count = 0

    for team in not_1540_speaker:
        speaker_acc_noavg = get_speaker_acc_noavg()
        speaker_comparison_raw_data[team] = speaker_acc_noavg[count]
        count = count + 1

    speaker_comparison_data = sorted(speaker_comparison_raw_data.items(), key=operator.itemgetter(1))
    speaker_comparison_data = dict(sorted(speaker_comparison_raw_data.items(), key=operator.itemgetter(1), reverse=True))

    speaker_comparison_keys = [key for key in list(speaker_comparison_data.keys())]
    speaker_comparison_values = [value for value in list(speaker_comparison_data.values())]
    
    return speaker_comparison_values

def speaker_color_filter(speaker_comparison_keys):    
    speaker_colors = []

    for key in speaker_comparison_keys:
        if key == '1540':
            speaker_colors.append("rgb(255,193,69)")
        else: 
            speaker_colors.append("rgb(195,195,195)")
            
    return speaker_colors

def get_speaker_comparison_graph():
    ampfig = go.Figure(go.Bar(x=get_speaker_comparison_keys(), y=get_speaker_comparison_values(), marker_color=speaker_color_filter(get_speaker_comparison_keys())))
    ampfig.update_layout(plot_bgcolor='rgb(28, 28, 28)')
    ampfig.update_layout(paper_bgcolor='rgb(28, 28, 28)')
    ampfig.update_layout(font=dict(color="white", size=14, family = "Poppins"))
    ampfig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    ampfig.update_layout(barmode='group')
    ampfig.update_xaxes(title_text="Speaker Comparison", title_font=dict(color="white", family="Poppins"))
    amp_html = ampfig.to_html (
        include_plotlyjs=True, 
        full_html=False,
        
    )
    return amp_html        

def get_amp_comparison_keys():
    not_1540_amp = []
    count = 0 

    for team in teams:
        if team == ('1540',):
            not_1540_amp.append('1540')
        else:
            not_1540_amp.append(f"{count}")
            count = count + 1

    amp_comparison_raw_data = {}       
    count = 0

    for team in not_1540_amp:
        amp_acc_noavg = get_amp_acc_noavg()
        amp_comparison_raw_data[team] = amp_acc_noavg[count]
        count = count + 1

    amp_comparison_data = sorted(amp_comparison_raw_data.items(), key=operator.itemgetter(1))
    amp_comparison_data = dict(sorted(amp_comparison_raw_data.items(), key=operator.itemgetter(1), reverse=True))

    amp_comparison_keys = [key for key in list(amp_comparison_data.keys())]
    amp_comparison_values = [value for value in list(amp_comparison_data.values())]
    
    return amp_comparison_keys

def get_amp_comparison_values():
    not_1540_amp = []
    count = 0 

    for team in teams:
        if team == ('1540',):
            not_1540_amp.append('1540')
        else:
            not_1540_amp.append(f"{count}")
            count = count + 1

    amp_comparison_raw_data = {}       
    count = 0

    for team in not_1540_amp:
        amp_acc_noavg = get_amp_acc_noavg()
        amp_comparison_raw_data[team] = amp_acc_noavg[count]
        count = count + 1

    amp_comparison_data = sorted(amp_comparison_raw_data.items(), key=operator.itemgetter(1))
    amp_comparison_data = dict(sorted(amp_comparison_raw_data.items(), key=operator.itemgetter(1), reverse=True))

    amp_comparison_keys = [key for key in list(amp_comparison_data.keys())]
    amp_comparison_values = [value for value in list(amp_comparison_data.values())]
    
    return amp_comparison_values

def amp_color_filter(amp_comparison_keys):
    amp_colors = []

    for key in amp_comparison_keys:
        if key == '1540':
            amp_colors.append("rgb(255,193,69)")
        else: 
            amp_colors.append("rgb(195,195,195)")
            
    return amp_colors

def get_amp_comparison_graph(toggle, html):
    ampfig = go.Figure(go.Bar(x=get_amp_comparison_keys(), y=get_amp_comparison_values(), marker_color=amp_color_filter(get_amp_comparison_keys())))
    ampfig.update_layout(plot_bgcolor='rgb(28, 28, 28)')
    ampfig.update_layout(paper_bgcolor='rgb(28, 28, 28)')
    ampfig.update_layout(font=dict(color="white", size=14, family = "Poppins"))
    ampfig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    ampfig.update_layout(barmode='group')
    ampfig.update_xaxes(title_text="Amp Comparison", title_font=dict(color="white", family="Poppins"))
    amp_html = ampfig.to_html (
        include_plotlyjs=True, 
        full_html=False,
        
    )
    return amp_html
def get_amp_graph(toggle, html):
    if toggle:
        if html:
            # if get_amp_acc()[0] >= 0.90 and get_amp_acc()[0] > get_amp_acc()[1]:
                    ampfig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_amp_acc(), marker_color=["rgb(255,193,69)", "rgb(195,195,195)"]))
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
                # return "bad"
        else: return get_amp_acc()
    else:
        return "bad"
def get_speaker_graph(toggle, html):
    if toggle:
        if html:
            # if get_speaker_acc()[0] >= 0.90 and get_speaker_acc()[0] > get_speaker_acc()[1]:
                speakerfig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_speaker_acc(), marker_color=["rgb(255,193,69)", "rgb(195,195,195)"]))
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
        else: return get_speaker_acc()
    else:
        return "bad"
def auto_acc_graph(toggle, html):
    if toggle:
        if html:
            # if get_auto_acc()[0] >= 0.70 and get_auto_acc()[0] > get_auto_acc()[1]:
                autofig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_auto_acc(), marker_color=["rgb(255,193,69)", "rgb(195,195,195)"]))
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
                # return "bad"
        else: return get_auto_acc()
    else: return "bad"
def get_broke_graph(toggle):
    if toggle:
            if get_broke() == False:
                return "<h4>Team 1540's robot has broken</h4><h3>0<h3><h4> times this competition</h4>"
            else:
                return "bad"
    else: return "bad"
def get_total_auto(toggle, html): # needs benchmark
    if toggle:
        postgresSQL_1540_autospeaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_1540_autospeaker_Query)
        speakerlist = cur.fetchall()
        speaker_total = 0
        for i in speakerlist:
            speaker_total +=i[0]
        postgresSQL_1540_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'""" 
        cur.execute(postgresSQL_1540_autoamp_Query)
        amplist = cur.fetchall()
        amp_total = 0
        for i in amplist:
            amp_total +=i[0]
        ampspeaker = amp_total + speaker_total
        if html:
            return f"<h4>Team 1540's robot has scored</h4><h3>{ampspeaker}<h3><h4> Notes during auto this event</h4>"
        else: return ampspeaker
    else: return "bad"
def get_total_whole(toggle, html): # needs benchmark
    if toggle:
        postgresSQL_1540_autospeaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_1540_autospeaker_Query)
        autospeakerlist = cur.fetchall()
        autospeaker_total = 0
        for i in autospeakerlist:
            autospeaker_total +=i[0]
        postgresSQL_1540_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'""" 
        cur.execute(postgresSQL_1540_autoamp_Query)
        amplist = cur.fetchall()
        autoamp_total = 0
        for i in amplist:
            autoamp_total +=i[0]
        autoampspeaker = autoamp_total + autospeaker_total
        
        
        postgresSQL_1540_telespeaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_1540_telespeaker_Query)
        telespeakerlist = cur.fetchall()
        telespeaker_total = 0
        for i in telespeakerlist:
            telespeaker_total +=i[0]
        postgresSQL_1540_teleamp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'""" 
        cur.execute(postgresSQL_1540_teleamp_Query)
        amplist = cur.fetchall()
        teleamp_total = 0
        for i in amplist:
            teleamp_total +=i[0]
        teleampspeaker = teleamp_total + telespeaker_total
        allampspeaker = teleampspeaker + autoampspeaker
        if html:
            return f"<h4>Team 1540's robot has scored</h4><h3>{allampspeaker}<h3><h4> Notes this event</h4>"
        else:
            return allampspeaker
    else: return "bad"
def get_total_whole_other(toggle, html):
    if toggle:
        autoampspeaker = 0
        for team in teams:
            postgresSQL_other_autospeaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
            cur.execute(postgresSQL_other_autospeaker_Query)
            autospeakerlist = cur.fetchall()
            autospeaker_total = 0
            for i in autospeakerlist:
                autospeaker_total +=i[0]
            postgresSQL_other_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'""" 
            cur.execute(postgresSQL_other_autoamp_Query)
            amplist = cur.fetchall()
            autoamp_total = 0
            for i in amplist:
                autoamp_total +=i[0]
            autoampspeaker += autoamp_total + autospeaker_total
        
        teleampspeaker = 0
        for team in teams:
            postgresSQL_other_telespeaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'"""
            cur.execute(postgresSQL_other_telespeaker_Query)
            telespeakerlist = cur.fetchall()
            telespeaker_total = 0
            for i in telespeakerlist:
                telespeaker_total +=i[0]
            postgresSQL_other_teleamp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}' AND match_key LIKE '{comp}%'""" 
            cur.execute(postgresSQL_other_teleamp_Query)
            amplist = cur.fetchall()
            teleamp_total = 0
            for i in amplist:
                teleamp_total +=i[0]
            teleampspeaker += teleamp_total + telespeaker_total
        allampspeaker = teleampspeaker + autoampspeaker
        if html:
            return f"<h4>Team 1540's robot has scored</h4><h3>{allampspeaker}<h3><h4> Notes this event</h4>"
        else:
            return allampspeaker
    else: return 
def times_climb(toggle, html):
    if toggle:
        postgresSQL_1540_climb_Query = f"""SELECT stage_enum FROM "TeamMatches" WHERE team_key='1540' AND match_key LIKE '{comp}%'"""
        cur.execute(postgresSQL_1540_climb_Query)
        stage = cur.fetchall()
        #i need help with enums!!!
    else: return "bad"
def message1(toggle):
    if toggle: return "<h2>Thank You</h2><h4>for visiting team 1540's pits</h4>"
    else: return "bad"
def message2(toggle):
    if toggle: return "<h4>We appreciate</h4><h2>YOU</h2><h4>for joining us in our pits</h4>"
    else: return "bad"
def percent_by_us(toggle, html): # needs benchmark
    if toggle:
        percent = round(get_total_whole(True, False) / get_total_whole_other(True, False), 3) * 100
        if html: return f"<h4>Team 1540's robot has scored</h4><h3>{percent}%</h3><h4>of the notes scored this event</h4>"
        else: return percent
    else: return "bad"
def total_shots(toggle, html):
    if toggle:
        big_total = 0
        
        #SPEAKER
        postgresSQL_1540_autospeaker_Query = f"""SELECT auto_speaker_succeed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_autospeaker_Query)
        autospeakerlist = cur.fetchall()
        for i in autospeakerlist:
            big_total +=i[0]
        postgresSQL_1540_autospeaker_missed_Query = f"""SELECT auto_speaker_missed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_autospeaker_missed_Query)
        autospeakerlistmissed = cur.fetchall()
        for i in autospeakerlistmissed:
            big_total +=i[0]
        postgresSQL_1540_telespeaker_missed_Query = f"""SELECT tele_speaker_missed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_telespeaker_missed_Query)
        telespeakerlistmissed = cur.fetchall()
        for i in telespeakerlistmissed:
            big_total +=i[0]
        postgresSQL_1540_telespeaker_Query = f"""SELECT tele_speaker_succeed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_telespeaker_Query)
        telespeakerlist = cur.fetchall()
        for i in telespeakerlist:
            big_total +=i[0]
        
        
        #AMP
        postgresSQL_1540_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_autoamp_Query)
        autoamplist = cur.fetchall()
        for i in autoamplist:
            big_total +=i[0]
        postgresSQL_1540_autoamp_missed_Query = f"""SELECT auto_amp_missed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_autoamp_missed_Query)
        autoamplistmissed = cur.fetchall()
        for i in autoamplistmissed:
            big_total +=i[0]
        postgresSQL_1540_teleamp_missed_Query = f"""SELECT tele_amp_missed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_teleamp_missed_Query)
        teleamplistmissed = cur.fetchall()
        for i in teleamplistmissed:
            big_total +=i[0]
        postgresSQL_1540_teleamp_Query = f"""SELECT tele_amp_succeed FROM "TeamMatches" WHERE team_key='1540'"""
        cur.execute(postgresSQL_1540_teleamp_Query)
        teleamplist = cur.fetchall()
        for i in teleamplist:
            big_total +=i[0]
        
        if html: return f"<h4>Team 1540's robot has made</h4><h3>{big_total}<h3><h4>shots this season</h4>"
        else: return big_total
    else: return "bad"
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
def chicken_weight(toggle):
    if toggle: return '<h4>The heaviest chicken was 22lbs! That is</h4><h3>88 lbs</h3><h4>less than the weight of our robot!</h4>'
    else: return 'bad'
def event_total_score(toggle, html):
    if toggle:
        event_tot = get_total_whole(True, False) + get_total_whole_other(True, False)
        if html: return f'<h4>There has been</h4><h3>{event_tot}</h3><h4>notes scored this event</h4>'
        else: return event_tot
    else: return 'bad'
def make_graph() -> str:

    
    listofresults=[total_shots(toggle_list[8], True), get_trap_graph(toggle_list[2], True), get_amp_graph(toggle_list[0], True), get_speaker_graph(toggle_list[1], True), message2(toggle_list[5]), auto_acc_graph(toggle_list[3], True), get_broke_graph(toggle_list[10]), get_total_auto(toggle_list[6], True), get_total_whole(toggle_list[7], True), message1(toggle_list[4]), percent_by_us(toggle_list[9] ,True), eggs_in_season(toggle_list[11], True), chicken_weight(toggle_list[12]), event_total_score(toggle_list[13], True)]
    # listofresults=[eggs_in_season(toggle_list[11], True)]
    reallist = []
    for result in listofresults:
        if result != "bad":
            reallist.append(result)
    return reallist
toggle_list = [False, False, False, False, True, True, False, False, False, False, False, True, True, True]
@app.route("/")
def index():
    return render_template('hensight.html')
@app.route('/request')
def main():
    global listindex
    html = make_graph()
    if len(html)-1 > listindex:
        listindex +=1
    else:
        listindex = 0
    return html[listindex]

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/fet', methods = ['POST'])
def dashrequest():
    global toggle_list
    toggle_list = request.json
    return "hi"
@app.route('/feet')
def dashget():
    datalist = [get_amp_graph(True, False), get_speaker_graph(True, False), get_trap_graph(True, False), auto_acc_graph(True, False), '', '', get_total_auto(True, False), get_total_whole(True, False), total_shots(True, False), percent_by_us(True, False), 'Automatic', eggs_in_season(True, False), event_total_score(True,False)]
    return datalist
@app.route('/gitfeet')
def gitfeet():
    return '<marquee><h4 style="font-size: 30px">GIT FEET</h4><h4 style="font-size: 30px">GIT FEEt</h4><h4 style="font-size: 30px">GIT FEET</h4><h4 style="font-size: 30px">GIT FEEt</h4><h4 style="font-size: 30px">GIT FEET</h4></marquee>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)