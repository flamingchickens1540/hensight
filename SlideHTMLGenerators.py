import time

from main import hensightStats


def thank_msg(toggle):
    if toggle:
        return '<h4>Team 1540 Thanks</h4><h3>YOU</h3><h4>for joining us in our pits!</h4>'
    else:
        return 'bad'


def eggs_in_match(toggle):
    if toggle:
        return "<h4>During each match over</h4><h2 style='font-size:13rem;'i>520,000</h2><h4>eggs are laid in the US!</h4>"
    else:
        return 'bad'


def feather_message(toggle):
    if toggle:
        return "<h4>There are as many people that do FIRST as feathers on </h4><h2>Ten and Half chickens!</h2>"
    else:
        return 'bad'


def chicken_notes(toggle):
    if toggle:
        return "<h4>A chicken of the non-flaming variety is expected to score</h4><h3>0</h3><h4>notes during a match!</h4>"
    else:
        return 'bad'


def chicken_weight(toggle):
    if toggle:
        return '<h4>The heaviest chicken was 22lbs! That is</h4><h3>88 lbs</h3><h4>less than the weight of our robot!</h4>'
    else:
        return 'bad'


def eggs_in_season(toggle, html):
    if toggle:
        current_time = round(time.time())
        secconds_passed = round(current_time - 1704571200)
        years = secconds_passed / 31536000
        eggs_laied = round(years * 250)
        if html:
            return f'<h4>A single chicken would have laid</h4><h3>{eggs_laied}</h3><h4>eggs since build season started</h4>'
        else:
            return eggs_laied
    else:
        return 'bad'


def robo_name(toggle):
    if toggle:
        return "<h4>Our robot is named Fried Egg because</h4><h2>We're cooking</h2><h4>this year!</h4>"
    else:
        return 'bad'


def chicken_foul():
    return "<h1 style='font-size:1.5rem;'>However, in the whimsical scenario where we decide to replace the robot on the field with a live chicken, a cascade of unforeseen consequences would likely unfold. Picture this: amidst the high-stakes game, the unsuspecting chicken, blissfully unaware of the intricate rules governing the match, would likely become the unwitting perpetrator of an array of tech fouls. The referee, undoubtedly perplexed by the surreal turn of events, might find themselves compelled to brandish a red card, signaling not only an expulsion from the game but also drawing attention to the peculiar nature of the infringement.</h1>"


def chicken_noise(toggle):
    if toggle:
        return "<h4>Chickens can squawk as loud as</h4><h2>70 decibels<h2><h4>about as loud as the average classroom</h4>"
    else:
        return 'bad'


def chicken_eat(toggle):
    if toggle:
        return '<h4>FRC Students eat approximately</h4><h3 style="font-size: 11rem;">7,917,000</h3><h4>chickens per year</h4>'
    else:
        return 'bad'


def chicken_cycles(toggle):
    if toggle:
        return '<h4>A chicken of the non-flaming variety can make a speaker cycle in</h4><h2>3 seconds!</h2>'
    else:
        return 'bad'


def battery(toggle):
    if toggle:
        return '<h5>A chicken running on a hamster wheel would take</h5><h3 style="font-size:13rem;">5 hours</h3><h5>to generate enough power for a ES 17-12 battery</h5>'
    else:
        return 'bad'


def logodvd(toggle):
    if toggle:
        return '<marquee class="marquee" behavior="alternate" direction="down"scrollamount="20" id="logo"><marquee style="margin-bottom: 160px" behavior="alternate" width="100%" scrollamount="20"><img width="250px" src="https://avatars.githubusercontent.com/u/5280254?s=200&v=4" alt="dvd" id="spin"></marquee></marquee><p id="msg">inside of my head rn</p>'
    else:
        return 'bad'


def event_total_notes(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h4>There has been</h4><h3>{"{:,}".format(round(hensightStats.hensight_stats["event_total_notes"]))}</h3><h4>notes scored at this event</h4>'
    else:
        return 'bad'


def event_trap_notes(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h4>Teams have scored</h4><h3>{round(hensightStats.hensight_stats["event_trap_notes"])}</h3><h4>notes in the trap at this event</h4>'
    else:
        return 'bad'


def event_high_score(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h4>The high score at this event is</h4><h3>{round(hensightStats.hensight_stats["event_high_score"])}</h3><h4>points! (good job)</h4>'
    else:
        return 'bad'


def spotlight_percent(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h1>At this competition</h1><h3>{round(hensightStats.hensight_stats["event_spotlight_note_percentage"], 2)}%<h3><h1>of robotics have been spotlit</h1><div></div><h1>In the world</h1><h3>{round(hensightStats.hensight_stats["global_spotlight_note_percentage"], 2)}%</h3><h1>of robots have been spotlit</h1>'
    else:
        return 'bad'


def global_total_notes(toggle):
    if toggle:
        return f'<h4>In the world</h4><h2>{"{:,}".format(round(hensightStats.hensight_stats["global_total_notes"]))}</h2><h4>notes have been scored</h4>'
    else:
        return 'bad'


def global_high_score(toggle):
    if toggle:
        return f"<h4>The global high score is</h4><h3>{round(hensightStats.hensight_stats["global_high_score"])}</h3><h4>points! That's a lot"
    else:
        return 'bad'


def event_speaker_notes(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h1>At this event, teams have scored</h1><h3>{"{:,}".format(round(hensightStats.hensight_stats["event_speaker_notes"]))}</h3><h1>notes in the speaker, while having scored</h1><h3>{round(hensightStats.hensight_stats["event_amplified_speaker_notes"])}</h3><h1>notes in an amplified speaker</h1>'
    else:
        return 'bad'


def global_amp_notes(toggle):
    if toggle:
        return f'<h4>Throughout the world</h4><h3 id="h7">{"{:,}".format(round(hensightStats.hensight_stats["global_amp_notes"]))}</h3><h4>notes have been scored in the amp</h4>'
    else:
        return 'bad'


def event_travel(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h4>Robots at this event have traveled</h4><h2>{"{:,}".format(round(hensightStats.hensight_stats["event_distance_traveled"]))}ft</h2><h4>in total :O</h4>'
    else:
        return 'bad'


def global_travel(toggle):
    if toggle:
        return f'<h4>All the robots in the world have traveled</h4><h2>{"{:,}".format(round(hensightStats.hensight_stats["global_distance_traveled"]))}ft</h2><h4>in total :O</h4>'

def event_alliance_score(toggle, event_toggle):
    if toggle and event_toggle:
        return f'<h4>At this event, the blue alliance has scored</h4><h2>{"{:,}".format(round(hensightStats.hensight_stats["event_blue_alliance_score"]))}</h2><h4>points combined</h4><h4>While the red alliance has scored</h4><h2>{"{:,}".format(round(hensightStats.hensight_stats["event_red_alliance_score"]))}</h2><h4>points combined</h4>'