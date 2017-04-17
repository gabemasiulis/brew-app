var hr = document.getElementById('hr');
var mn = document.getElementById('mn');
var sec = document.getElementById('sec');
var display = document.getElementById('timer');
var recipeName = document.getElementById('recipeName');
var current_step = document.getElementById('current_step');
var steps = localStorage['steps'];
var hop_adds = localStorage['hop_adds'];
var hopKeys = Object.keys(JSON.parse(hop_adds));


function hopCheck(time) {
    var sec = Math.floor(time / 1000);
    if (current_step.innerHTML == 'Boil' &&
        hopKeys.indexOf(sec.toString()) != -1) {
        alert(JSON.parse(hop_adds)[sec]);
    }
}

function setTimer() {
    // if a timer is running, stop it
    stopTimer();
    // we only set the timer if there is some value to set
    if (hr.value || mn.value || sec.value) {
        // the 450 adds a bump to ms and keeps the timer from skipping
        var remainingTime = (
            (Math.abs(Math.floor(hr.value)) * 3600000) +
            (Math.abs(Math.floor(mn.value)) * 60000) +
            (Math.abs(Math.floor(sec.value * 1000))) + 450
        );
        var resetTime = remainingTime;
        localStorage['remainingTime'] = remainingTime;
        localStorage['resetTime'] = resetTime;
        formatDisplay(remainingTime);
    }
}

function runTimer() {
    if (localStorage['isRunning']) {
        var endTime = Number(localStorage['endTime']);
        var remainingTime = endTime - Date.now();
        hopCheck(remainingTime);
        // adding some buffer time to make sure we don't lose any time
        if (remainingTime % 1000 < 10) {
            endTime += 441;
            localStorage['endTime'] = endTime;
        }
        localStorage['remainingTime'] = remainingTime;
        formatDisplay(remainingTime);
        if (remainingTime > 999) {
            timer = setTimeout(runTimer, 1000);
        } else {
            // make values falsey
            localStorage['isRunning'] = '';
            localStorage['remainingTime'] = '';
            localStorage['resetTime'] = '';
            nextTimer();
        }
    }
}

function formatDisplay(t) {
    var h = Math.floor(t/3600000);
    var m = Math.floor(t/60000) % 60;
    var s = Math.floor(t/1000) % 60;

    var displayHr = "0" + h;
    var displayMn = "0" + m;
    var displaySec = "0" + s;

    if (h > 0) {
        display.innerHTML = displayHr.slice(-2) + ":" + displayMn.slice(-2) + ":" + displaySec.slice(-2);
    } else {
        display.innerHTML = displayMn.slice(-2) + ":" + displaySec.slice(-2);
    }
}

function startTimer() {
    if (!localStorage['isRunning'] && localStorage['remainingTime']) {
        localStorage['isRunning'] = 'true';
        var remainingTime = Number(localStorage['remainingTime'])
        var endTime = Date.now() + remainingTime;
        localStorage['endTime'] = endTime;
        runTimer();
    }
}

function stopTimer() {
    localStorage['isRunning'] = '';
    clearTimeout(timer);
}

function resetTimer() {
    stopTimer();
    var remainingTime = localStorage['resetTime'];
    localStorage['remainingTime'] = remainingTime;
    formatDisplay(remainingTime);
}

function clearTimer() {
    stopTimer();
    localStorage['remainingTime'] = '';
    localStorage['resetTime'] = '';
    localStorage['endTime'] = '';
    var display = document.getElementById('timer').innerHTML = '00:00';
}

function nextTimer() {
    var index = Number(localStorage['stepIndex']);
    var parsed = JSON.parse(steps);
    index ++;
    if (localStorage['stepIndex'] && index < (parsed.length)) {
        stopTimer();
        current_step.innerHTML = parsed[index][0];
        mn.value = (parsed[index][1])
        localStorage['stepIndex'] = index;
        setTimer();
    }
}

if (localStorage['recipeLoaded']) {
    recipeName.innerHTML = localStorage['recipeName']
    nextTimer();
    localStorage['recipeLoaded'] = '';

} else {
    formatDisplay(localStorage['remainingTime']);
    var index = Number(localStorage['stepIndex'])
    var parsed = JSON.parse(steps);
    recipeName.innerHTML = localStorage['recipeName']
    current_step.innerHTML = parsed[index][0];
    runTimer();
}
