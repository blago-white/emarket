const changeUsernameForm = document.getElementById("change-username-form");
const username = document.getElementById("username-field");
const changeEmailForm = document.getElementById("change-email-form");
const email = document.getElementById("email-field");

let expanded = changeUsernameForm.style.display != "none";
let elements;

function expandInput(elem) {
    expanded = !expanded;

    elements = elem.id.split("-")[0] == "email" ? [changeEmailForm, email] : [changeUsernameForm, username];

    console.log(elements);

    elements[0].style.display = expanded ? "unset" : "none";
    elements[1].style.display = expanded ? "none" : "inline-flex"
}