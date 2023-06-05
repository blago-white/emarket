let VisibleNotifications = [];

function NotificationView(event) {
    const CurrentNotificationLabel = document.getElementById("notification-" + event.target.id.split("-")[event.target.id.split("-").length-1]);

    CurrentNotificationLabel.animate(
        [{"transform": CurrentNotificationLabel.style.transform == "scaleX(0)" ? "scaleX(1)" : "scaleX(0)"}],
        {duration: 200}
    )

    setTimeout(() => {
        CurrentNotificationLabel.style.transform = CurrentNotificationLabel.style.transform == "scaleX(0)" ? "scaleX(1)" : "scaleX(0)"
    }, 200)

}

function RergisterButtonsHandlers() {
    const NotificationLabels = document.getElementsByClassName("notification");

    for (notification in NotificationLabels) {
        try {
            NotificationLabels[notification].addEventListener("click", NotificationView);
        } catch {
        }
    }
}

RergisterButtonsHandlers()