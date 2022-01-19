const liveDataEndpoint = '/live-data';

let intervalFetchLiveStats = 0,
    intervalUpdateUI = 0;


$(function() {
    const delay = 5000;
    intervalFetchLiveStats = setInterval(fetchLiveStats, delay);
    intervalUpdateUI = setInterval(updateUI, delay);
})


function fetchLiveStats() {
    $.ajax({
        url: liveDataEndpoint
    }).done(function(data) {
        try {
            stats = data.live_stats || stats;
        } catch (e) {
            console.error(e);
            clearIntervals();
        }
    })
}


function updateUI() {
    if (!stats || !('blue' in stats) || !('red' in stats)) {
        return;
    }

    const blue = parseInt(stats.blue.mushrooms) || 0,
        red = parseInt(stats.red.mushrooms) || 0;

    if (blue === 0 && red === 0) {
        clearIntervals();
        console.log('Betting is closed at the moment PepeHands.');
        return;
    }

    const blueStr = blue.toLocaleString('en-US'),
        redStr = red.toLocaleString('en-US');

    updatePageTitle(blueStr, redStr);
    updatePageContents(blueStr, redStr);
}


function updatePageTitle(blueStr, redStr) {
    document.title = `Blue: ${blueStr} | Red: ${redStr}`;
}


function updatePageContents(blueStr, redStr) {
    $('#stats-blue-mushrooms').text(blueStr);
    $('#stats-red-mushrooms').text(redStr);
}


function clearIntervals() {
    clearInterval(intervalFetchLiveStats);
    clearInterval(intervalUpdateUI);
}