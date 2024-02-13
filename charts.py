from flask import Flask
import psycopg2
import plotly.graph_objects as go
import operator
from main import get_amp_acc, get_auto_acc, get_broke, get_speaker_acc, get_trap_number

def make_graph():

    if get_trap_number() != None:
        return "<h4>"+get_trap_number()+ "</h4>"

    def get_amp_graph():
        if get_amp_acc()[0] >= 0.90 and get_amp_acc()[0] > get_amp_acc()[1]:
            ampfig = go.Figure(go.Bar(x=['1540', 'Average'], y=get_amp_acc()))
            
        else:
            return None

   html = fig.to_html (
       include_plotlyjs=False,
       full_html=False,
   )


   return html
