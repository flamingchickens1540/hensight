import time
from HensightStatsManager import HensightStats

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
        return "<h4>A live chicken is expected to score</h4><h3>0</h3><h4>points during a match!</h4>"
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
    
def chicken_foul(toggle):
    if toggle: return "<h1 style='font-size:3rem;'>However, in the whimsical scenario where we decide to replace the robot on the field with a live chicken, a cascade of unforeseen consequences would likely unfold. Picture this: amidst the high-stakes game, the unsuspecting chicken, blissfully unaware of the intricate rules governing the match, would likely become the unwitting perpetrator of an array of tech fouls. The referee, undoubtedly perplexed by the surreal turn of events, might find themselves compelled to brandish a red card, signaling not only an expulsion from the game but also drawing attention to the peculiar nature of the infringement.</h1>"
    else: return "bad"

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
    
def trex(toggle):
    if toggle: return '<h4>Chickens are the closest living relatives to the </h4><h3>Tyrannosaurus rex.</h3>'
    else:return "bad"
    
def chicken_count(toggle):
    if toggle: return '<h4>There are more than </h4><h3>25 billion</h3><h4> chickens in the world, making them the most common bird species.</h4>'
    else: return "bad"

def chicken_eye(toggle):
    if toggle: return '<h4>Chickens have </h4><h3>three</h3><h4> eyelids per eye—an upper, lower, and a third transparent one.</h4>'
    else: return "bad"
    
def chicken_breed(toggle):
    if toggle: return '<h4>There are over </h4><h3>500</h3><h4> different chicken breeds worldwide.</h4>'
    else: return "bad"
    
def egg_time(toggle):
    if toggle: return '<h4>It takes a hen about </h4><h3>24–26</h3><h4> hours to lay a single egg.</h4>'
    else: return "bad"
    
def egg_pore(toggle):
    if toggle: return '<h4>The shell of an egg has about </h4><h3>7,000–17,000</h3><h4> tiny pores that allow air and moisture to pass through.</h4>'
    else: return "bad"
    
def points_scored(toggle):
    if toggle: return f'<h4>Throughout the season</h4><h3>{HensightStats["points_scored"]}</h3><h4>points have been scored'
    else: return "bad"
    
def average_points_permatch(toggle):
    if toggle: return f"<h4>On average an alliance scores</h4><h3>{HensightStats["average_points_permatch"]}</h3><h4>points per match</h4>"
    else: return "bad"
    
def penalty_points(toggle):
    if toggle: return f"<h4>This season there has been</h4><h3>{HensightStats["penalty_points"]}</h3><h4>foul points awarded</h4>"
    else: return "bad"

def auto_poitns(toggle):
    if toggle: return f"<h4>This season there has been</h4><h3>{HensightStats["auto_points"]}</h3><h4>points scored in auto</h4>"
    else: return "bad"

def percent_last_year(toggle):
    if toggle: return f"<h4>We are</h4><h3>{HensightStats["percent_last_year"]}%</h3><h4>of the way to scoring as many points as last year</h4>"
    else: return "bad"

def matches_played(toggle):
    if toggle: return f"<h4>This season</h4><h3>{HensightStats["matches_played"]}</h3><h4>matches have been played</h4>"
    else: return "bad"

def alliance_win_rate(toggle):
    if toggle:
        if HensightStats["red_win_count"] >= HensightStats["blue_win_count"]: return f"<h4>The red alliance is<h4><h3>{(HensightStats["red_win_count"] / HensightStats["blue_win_count"]) * 100}%</h3><h4>more likely to win any given match</h4>"
        else: return f"<h4>The blue alliance is<h4><h3>{(HensightStats["blue_win_count"] / HensightStats["red_win_count"]) * 100}%</h3><h4>more likely to win any given match</h4>"
    else: return "bad"
    
def event_algae_processed(toggle):
    if toggle: return f"<h4>At this event</h4><h3>{HensightStats["event_algae_processed"]}</h3><h4>algae have been processed</h4>"
    else: return "bad"
    
def event_rp_earned(toggle):
    if toggle: return f"<h4>At this event</h4><h3>{HensightStats["event_rp_earned"]}</h3><h4>RP have been earned</h4>"
    else: return "bad"


# HensightStats = {
#     "stacked_coral_event": 0, # to do
#     "average_coral_lvl": 0, # to do
#     "points_scored": 0,
#     "average_points_permatch": 0,
#     "penalty_points": 0,
#     "event_aglee_processed": 0, # to do
#     "event_rp_earned": 0, # to do
#     "auto_points": 0,
#     "percent_last_year": 0,
#     "blue_win_count": 0,
#     "red_win_count": 0,
#     "matches_played": 0
# }