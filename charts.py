from flask import Flask
import psycopg2
import plotly.graph_objects as go
import operator
from main import get_amp_acc, get_auto_acc, get_broke, get_speaker_acc, get_trap_number


# -------------------------------------------------------------------------------------------------------------------------#
#
#    THIS FILE IS NOT IN USE
#
# -------------------------------------------------------------------------------------------------------------------------#
def make_graph():

    def get_trap_graph():
        if get_trap_number() != None:
            return "<h4>" + get_trap_number() + "</h4>"

    def get_amp_graph():
        if get_amp_acc()[0] >= 0.90 and get_amp_acc()[0] > get_amp_acc()[1]:
            ampfig = go.Figure(go.Bar(x=["1540", "Average"], y=get_amp_acc()))
            amp_html = ampfig.to_html(
                include_plotlyjs=False,
                full_html=False,
            )
            return amp_html

    def get_speaker_graph():
        if get_speaker_acc()[0] >= 0.90 and get_speaker_acc()[0] > get_speaker_acc()[1]:
            speakerfig = go.Figure(go.Bar(x=["1540", "Average"], y=get_speaker_graph()))
            speaker_html = speakerfig.to_html(
                include_plotlyjs=False,
                full_html=False,
            )
            return speaker_html

    def auto_acc_graph():
        if get_auto_acc()[0] >= 0.70 and get_auto_acc()[0] > get_auto_acc()[1]:
            autofig = go.Figure(go.Bar(x=["1540", "Average"], y=get_auto_acc()))
            auto_html = autofig.to_html(
                include_plotlyjs=False,
                full_html=False,
            )

    def get_broke_graph():
        if get_broke() == True:
            return None
        else:
            return "<h4>0</h4>"

    listofresults = [
        get_trap_graph(),
        get_amp_graph(),
        get_speaker_graph(),
        auto_acc_graph(),
        get_broke_graph(),
    ]
    reallist = []
    for result in listofresults:
        if result != None:
            reallist.append(result)
    return get_amp_graph()
