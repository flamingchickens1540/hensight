let elem = document.documentElement;
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        /* IE11 */
        elem.msRequestFullscreen();
    }
}

function getTime() {
    let d = new Date();
    let hours = d.getHours();
    let mins = d.getMinutes();
    let sec = d.getSeconds();
    let cycle = ' AM'
    if (hours > 12){
        hours -= 12
        cycle = " PM"
    }
    let h = ("00" + hours).slice(-2);
    let m = ("00" + mins).slice(-2);
    let s = ("00" + sec).slice(-2);
    let time = h + ":" + m + ":" + s + cycle;
    document.getElementById("time").innerHTML = time;
}


function getColor(value){
    //value from 0 to 1
    var hue=((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}