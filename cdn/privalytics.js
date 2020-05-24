function beat(secret_id) {
    if (document.visibilityState === 'visible') {
        var data = {secret_id: secret_id};
        var request = new XMLHttpRequest();
        request.open('POST', 'https://www.privalytics.io/api/beat', true);
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        request.send(JSON.stringify(data));
    }
}

function privalytics(privalytics_id) {
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
            var secret_id = this.response.id;
            var intervalID = setInterval(function () {
                beat(secret_id);
            }, 20000);
        }
    };
    request.send(JSON.stringify(data));
}

privalytics(privalytics_id);
