from flask import Flask
import psycopg2
import plotly.graph_objects as go

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

autoamps = []

for team in teams:
    postgresSQL_autoamp_Query = f"""SELECT auto_amp_succeed FROM "TeamMatches" WHERE team_key='{team[0]}'"""
    cur.execute(postgresSQL_autoamp_Query)
    autoamps = list.append([team, cur.fetchall()])
    print("autoamps")
    print(autoamps)

print("after")
print(autoamps)
fig = go.Figure([go.Bar (x=autoamps[0], y=autoamps[1])])
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
# cur.close()
# conn.close()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    port = 8000
    app.run(host='0.0.0.0')