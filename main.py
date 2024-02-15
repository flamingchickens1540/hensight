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
except psycopg2.OperationalError:
    print(f"Unable to connect to database. Are you SSHed? Error: {sys.exc_info()[0]}")
    quit(0)

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
