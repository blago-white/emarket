const setterButton = document.getElementById("stortage-setter");
const choicesList = document.getElementById("stortage-setter-choices-expand");
const setterText = document.getElementById("setter-text");

let expanded = false;

function choicesAction(event) {
    if (event.target.id != "stortage-setter" && event.target.id != "setter-text") {
        return
    }

    expanded = !expanded;
    choicesList.style.transform = expanded ? "translateY(0%)" : "translateY(100%)";
    setterText.style.transform = expanded ? "translateY(0%)" : "translateY(100%)";
}

function choiceActivate(choiceValue) {
    let url = new URL(document.location.href);

    if (url.searchParams.has("stortage") && url.searchParams.getAll("stortage").includes(String(choiceValue))) {
        url.href = url.href.replace("stortage="+choiceValue, "");
    } else {
        url.searchParams.append("stortage", choiceValue);
    }

    url.searchParams.set("page", "1");
    url.searchParams.set("filters", "1")

    document.location.href = url.href;
}

setterButton.addEventListener("click", choicesAction);
