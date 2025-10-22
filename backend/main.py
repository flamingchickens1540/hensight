from flask import Flask
from internal import schedule

app = Flask(__name__)

#INTERNAL ROUTES

@app.route("/getSchedule")
def getSchedule():
    return schedule.getSchedule()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True, use_reloader=False)