const checkboxLabel = document.getElementById("checkbox-label");
const checkboxMark = document.getElementById("check-mark");
const passwordInput = document.getElementById("id_password");

let active = false;
let transform = false;


function checkboxAction(event) {
    active = !active;

    if (active) {
        transform = "translateX(50%) rotate(0deg) scale(1)";
    } else {
        transform = "translateX(0%) rotate(-45deg) scale(0)";
    }

    checkboxLabel.childNodes[1].classList.toggle("checkbox-remember-active");
    checkboxLabel.style.width = active ? "7.9em" : "6.5em";
    checkboxMark.style.transform = transform;
}

function changePasswordToTextInput() {
    passwordInput.type = "text";
}

changePasswordToTextInput();
checkboxLabel.addEventListener("click", checkboxAction);
