const ConfirmWindow = document.getElementsByClassName("confirm-window-wrapper")[0];
const DeleteForm = document.getElementById("delete-form")
let ConfirmWindowIsVisible = false;
let FromButtonId;

function OpenConfirmWindow(event) {
    if (ConfirmWindowIsVisible || !event.target.id) {return}

    DeleteForm.action = DeleteForm.action.split('/').slice(0, -1).join('/') + "/" + event.target.id

    ConfirmWindow.style.opacity = "1";
    ConfirmWindowIsVisible = true;

    setTimeout(() => {ConfirmWindow.style.display = "flex"}, 200)
}

function HideConfirmWindow(event) {
    if (!ConfirmWindowIsVisible || event.target.id != "cancel") {return}

    ConfirmWindow.style.opacity = "0";
    ConfirmWindowIsVisible = false;

    setTimeout(() => {ConfirmWindow.style.display = "none"}, 200)
}

function RergisterButtonsHandlers() {
    ButtonsDelete = document.getElementsByClassName("user-card-delete-card");
    for (button in ButtonsDelete) {
        try {
            ButtonsDelete[button].addEventListener("click", OpenConfirmWindow);
        } catch {}
    }
}

RergisterButtonsHandlers()

ButtonCancel = document.getElementsByClassName("user-card-cancel-card")[0];
ButtonCancel.addEventListener("click", HideConfirmWindow);
