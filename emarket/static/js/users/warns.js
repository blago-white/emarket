let nowWarnWindowDisplayed = false;
const warn_window_full_screen = document.getElementById("full-screen-warn-canvas");


function ChangeVisibilityWarnClick(event) {
    const targetElementId = event.target.parentElement.id;

    if (event.pointerType == "mouse") {
        ChangeDisplaySmallErrorField(event, targetElementId)
    } else {ChangeDisplayFullScreenErrorField(event, targetElementId)}

    nowWarnWindowDisplayed = !nowWarnWindowDisplayed;
}

function ResetFullScreenWarnWindowDisplay (event) {
    nowWarnWindowDisplayed = false;
    ChangeDisplayFullScreenErrorField(event);
}

function ChangeDisplayFullScreenErrorField(event, targetElementId) {
    warn_window_full_screen.classList.toggle("warn-canvas-hidden");
    document.getElementById("canvas-content").innerHTML = document.getElementById("warn-text-" + targetElementId).innerHTML;
}


function ChangeDisplaySmallErrorField(event, targetElementId) {
    warn_window = document.getElementById("warn-window-" + targetElementId);
    const target_opacity = nowWarnWindowDisplayed ? "0" : "1";

    warn_window.animate({"opacity": target_opacity},
                        {duration: 200})

    if (!nowWarnWindowDisplayed) {
        warn_window.style.display = "unset";
        setTimeout(e => {
            warn_window.style.opacity = target_opacity;
        }, 200);
    }

    else if (nowWarnWindowDisplayed) {
        setTimeout(e => {
            warn_window.style.display = "none";
            warn_window.style.opacity = target_opacity;
        }, 200);
    }
}

function RegisterSmallErrorFieldsHandlers(elements) {
    for (warn in elements) {
        try {
            elements[warn].addEventListener("click", ChangeVisibilityWarnClick);
        } catch {}
    }
}

RegisterSmallErrorFieldsHandlers(document.getElementsByClassName("warnings"));

warn_window_full_screen.addEventListener("click", ResetFullScreenWarnWindowDisplay);
