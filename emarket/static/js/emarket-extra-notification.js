const REQUEST_PATH = '/accounts/delivered/';

function sendUserNotified(userip) {
    sendUserNotifiedRequest();
    document.getElementById('emarket-notification-body').style.display = 'none';
}

function sendUserNotifiedRequest() {
    fetch(REQUEST_PATH, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    })
}
