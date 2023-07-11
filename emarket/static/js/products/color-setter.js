const colorSetterButton = document.getElementById("color-setter");
const colorschoicesList = document.getElementById("color-setter-choices-expand");
const colorSetterText = document.getElementById("color-setter-text");

let colorsExpanded = false;

function choicesAction(event) {
    if (event.target.id != "color-setter" && event.target.id != "color-setter-text") {
        return
    }

    colorsExpanded = !colorsExpanded;
    colorschoicesList.style.transform = colorsExpanded ? "translateY(0%)" : "translateY(100%)";
    colorSetterText.style.transform = colorsExpanded ? "translateY(0%)" : "translateY(100%)";
}

function choiceActivateColor(choiceValue) {
    let url = new URL(document.location.href);

    if (url.searchParams.has("color") && url.searchParams.getAll("color").includes(String(choiceValue))) {
        url.href = url.href.replace("color="+choiceValue, "");
    } else {
        url.searchParams.append("color", choiceValue);
    }

    url.searchParams.set("page", "1");
    url.searchParams.set("filters", "1")

    document.location.href = url.href;
}

colorSetterButton.addEventListener("click", choicesAction);
