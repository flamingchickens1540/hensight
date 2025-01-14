import time

def eggs_in_season(toggle):
    if toggle:
        current_time = round(time.time())
        secconds_passed = round(current_time - 1736020800)
        years = secconds_passed / 31536000
        eggs_laied = round(years * 250)
        return f"<h4>A single chicken would have laid</h4><h3>{eggs_laied}</h3><h4>eggs since build season started</h4>"
    else:
        return "bad"