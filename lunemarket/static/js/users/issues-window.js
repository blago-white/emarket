const issuesButton = document.getElementById("issues-button");
const issues = document.getElementById("issues");
let expanded = false;

function issuesWindow(event) {
    expanded = !expanded;
    issues.style.width = expanded ? "8em" : "0px";
    issues.style.fontSize = expanded ? "1em" : "0em";
    issuesButton.style.width = expanded ? "9.5em" : "1.6em";
}

issuesButton.addEventListener("click", issuesWindow);