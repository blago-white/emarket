let visibleNotificationsDictIds = new Map();
let currentNotificationDetails;
let newDisplayValue;

const changeDisplayButtonImage = document.getElementById("change-display-button-img");

function changeNotificationDetails(event, notificationId) {
    newDisplayValue = !(typeof visibleNotificationsDictIds.get(notificationId)=="boolean" ? visibleNotificationsDictIds.get(notificationId) : false);
    visibleNotificationsDictIds.set(notificationId, newDisplayValue);

    currentNotificationDetails = document.getElementById("notification-"+notificationId);
    currentNotificationDetails.style.height = newDisplayValue ? "auto" : "0em";
    currentNotificationDetails.style.padding = newDisplayValue ? ".5em" : "0em";

    document.getElementById("change-display-button-img-"+notificationId).style.transform = newDisplayValue ? "rotate(-90deg)" : "rotate(90deg)";
}
