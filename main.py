from flask import Flask
import psycopg2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import operator

app = Flask(__name__)


# Define the connection parameters
host = "127.0.0.1"
port = 5432
database = "crescendo_scouting"
user = "chargedup_scouting_analysis"
password = "amptrapspeaker1540"

# Connect to the database
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password,
)

# Create a cursor
cur = conn.cursor()

postgresSQL_team_Query = 'SELECT team_key FROM "Teams"'
cur.execute(postgresSQL_team_Query)
teams = cur.fetchall()


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
    amp_acc.append(round(sec_final_average / mis_final_average))
    return amp_acc
sec_average_ampacc = {}
mis_average_ampacc = {}
amp_acc = []

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
    speaker_acc.append(round(sec_final_average / mis_final_average))
    return speaker_acc
sec_average_speakeracc = {}
mis_average_speakeracc = {}
speaker_acc = []

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

def get_trap_number():
    postgresSQL_1540_trap_Query = f"""SELECT trap_succeed FROM "TeamMatches" WHERE team_key='1540'"""
    cur.execute(postgresSQL_1540_trap_Query)
    trapnumber = cur.fetchall()
    total = 0
    trapnumber = round(total / len(trapnumber), 2)
    if trapnumber > 0:
        return trapnumber

def get_broke():
    postgresSQL_broke_Query = """SELECT is_broke FROM "TeamMatches" WHERE team_key='1540' AND is_broke='True'"""
    cur.execute(postgresSQL_broke_Query)
    broke = cur.fetchall()
    if broke == "[]":
        return True
    else:
        return False
    
print(get_auto_acc())


    # print(team, total)
    # print(autoamps[team])
    # autoamps[team] = cur.fetchall()


# keys = [key[0] for key in list(descending_autoamps.keys())]
# values = [value for value in list(descending_autoamps.values())]

# print(keys)
# print(values)

# fig = make_subplots(rows=2, cols=1)

# fig.add_trace(go.Bar(x=keys, y=values), row=1, col=1)
# fig.add_trace(go.Bar(x=values, y=keys), row=2, col=1)

# fig.update_layout(
#     autosize=False,
#     width=1000,
#     height=1000,
#     margin=dict(
#         l=50,
#         r=50,
#         b=100,
#         t=100,
#         pad=4
#     ),
#     paper_bgcolor="LightSteelBlue",
# )

# fig.show()




# # Execute a query
# postgreSQL_select_Query = 'SELECT team_key, auto_amp_succeed FROM "TeamMatches"'
# cur.execute(postgreSQL_select_Query)

# teamnames_Query = 'SELECT team_key FROM "Teams"'
# cur.execute(teamnames_Query)



# # Get the results
# rows = cur.fetchmany(50)

# print(rows)

# teamnums = [row[0] for row in rows]
# autoamps = [row[1] for row in rows]



# fig = go.Figure([go.Bar (x=teamnums, y=autoamps)])
# fig.show()

# Close the cursor and the connection
cur.close()
conn.close()

@app.route("/")
def hello_world():
    return "<p>Goodbye, World!</p>" 

if __name__ == '__main__':
    app.run(host='0.0.0',port=5001,debug=True)