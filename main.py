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

autoamps = {}

for team in teams:
    postgresSQL_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
    cur.execute(postgresSQL_autoamp_Query)
    datapoints = cur.fetchall()   
    print(datapoints)
    total = 0

    for datapoint in datapoints:
        total += datapoint[0]

        autoamps[team] = round(total / len(datapoints), 2)


descending_autoamps = sorted(autoamps.items(), key=operator.itemgetter(1))
descending_autoamps = dict( sorted(autoamps.items(), key=operator.itemgetter(1), reverse=True))

    # print(team, total)
    # print(autoamps[team])
    # autoamps[team] = cur.fetchall()


keys = [key[0] for key in list(descending_autoamps.keys())]
values = [value for value in list(descending_autoamps.values())]

print(keys)
print(values)

fig = make_subplots(rows=2, cols=1)

fig.add_trace(go.Bar(x=keys, y=values), row=1, col=1)
fig.add_trace(go.Bar(x=values, y=keys), row=2, col=1)

fig.update_layout(
    autosize=False,
    width=1000,
    height=1000,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)

fig.show()




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
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    port = 8000
    app.run(host='0.0.0.0')