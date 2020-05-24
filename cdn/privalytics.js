var beat = function (secret_id) {
    var data = {id: secret_id};
    var request = new XMLHttpRequest();
    request.open('POST', 'https://www.privalytics.io/api/beat', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
}

var privalytics = function (privalytics_id) {
    if (!window) return;
    var url = window.location;
    var document = window.document;
    var navigator = window.navigator;

    var data = {url: url.href};
    if (document.referrer) data.referrer = document.referrer;
    if (window.innerWidth) data.screen_width = window.innerWidth;
    if (window.innerHeight) data.screen_height = window.innerHeight;
    // If do not track is enabled, we wont store any personal information on our servers
    data.dnt = ('doNotTrack' in navigator && navigator.doNotTrack === "1");
    data.account_id = privalytics_id;

    var request = new XMLHttpRequest();
    request.open('POST', 'https://www.privalytics.io/api/tracker', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.responseType = 'json';
    request.onload = function (e) {
        if (this.status === 200) {
            console.log('response', this.response); // JSON response
            console.log('id', this.response.id);
            var secret_id = this.response.id;
            var timer = new TaskTimer(20000);
            timer.addTask({
                name: 'beat',
                tickInterval: 1,    // run every 1 ticks
                totalRuns: 0,
                callback: function (task) {
                    beat(secret_id);
                }
            });
        }
    };
    request.send(JSON.stringify(data));
    return response.id;
};
privalytics(privalytics_id);
