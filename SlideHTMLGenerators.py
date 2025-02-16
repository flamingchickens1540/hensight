import time
def thank_msg(toggle):
    if toggle:
        return (
            "<h4>Team 1540 Thanks</h4><h3>YOU</h3><h4>for joining us in our pits!</h4>"
        )
    else:
        return "bad"


def feather_message(toggle):
    if toggle:
        return "<h4>There are as many people that do FIRST as feathers on </h4><h2>10 1/2</h2><h4>chickens!</h4>"
    else:
        return "bad"


def chicken_notes(toggle):
    if toggle:
        return "<h4>A chicken of the non-flaming variety is expected to score</h4><h3>0</h3><h4>notes during a match!</h4>"
    else:
        return "bad"


def chicken_weight(toggle):
    if toggle:
        return "<h4>The heaviest chicken was 22lbs! That is</h4><h3>93 lbs</h3><h4>less than the weight of our robot!</h4>"
    else:
        return "bad"

def eggs_in_season(toggle):
    if toggle:
        current_time = round(time.time())
        secconds_passed = round(current_time - 1736020800)
        years = secconds_passed / 31536000
        eggs_laied = round(years * 250)
        return f"<h4>A single chicken would have laid</h4><h3>{eggs_laied}</h3><h4>eggs since build season started</h4>"
    else:
        return "bad"
    
def eggs_in_match(toggle):
    if toggle:
        return "<h4>Throughout the US</h4><h3>470,889</h3><h4>eggs are laid per match</h4>"
    else: return "bad"
    
def chicken_foul():
    return "<h1 style='font-size:3rem;'>However, in the whimsical scenario where we decide to replace the robot on the field with a live chicken, a cascade of unforeseen consequences would likely unfold. Picture this: amidst the high-stakes game, the unsuspecting chicken, blissfully unaware of the intricate rules governing the match, would likely become the unwitting perpetrator of an array of tech fouls. The referee, undoubtedly perplexed by the surreal turn of events, might find themselves compelled to brandish a red card, signaling not only an expulsion from the game but also drawing attention to the peculiar nature of the infringement.</h1>"


def chicken_noise(toggle):
    if toggle:
        return "<h4>Chickens can squawk as loud as</h4><h2>70 decibels<h2><h4>about as loud as the average classroom</h4>"
    else:
        return "bad"


def chicken_eat(toggle):
    if toggle:
        return '<h4>FRC Students eat approximately</h4><h3 style="font-size: 11rem;">7,917,000</h3><h4>chickens per year</h4>'
    else:
        return "bad"
    
def battery(toggle):
    if toggle:
        return '<h5>A chicken running on a hamster wheel would take</h5><h3 style="font-size:13rem;">5 hours</h3><h5>to generate enough power for a ES 17-12 battery</h5>'
    else:
        return "bad"


def logodvd(toggle):
    if toggle:
        return '<marquee class="marquee" behavior="alternate" direction="down"scrollamount="20" id="logo"><marquee style="margin-bottom: 160px" behavior="alternate" width="100%" scrollamount="20"><img width="250px" src="https://avatars.githubusercontent.com/u/5280254?s=200&v=4" alt="dvd" id="spin"></marquee></marquee><p id="msg">inside of my head rn</p>'
    else:
        return "bad"