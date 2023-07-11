let clicked = false;


function ChangeVisibilityWarnClick(event) {
    let warn_window;
    const target_element_id = event.target.parentElement.id;

    warn_window = document.getElementById(
        "warn-window-" + target_element_id
    );

    const target_opacity = clicked ? "0" : "1";
    warn_window.animate({"opacity": target_opacity},
                        {duration: 200})

    if (!clicked) {
        warn_window.style.display = "unset";
        setTimeout(e => {
            warn_window.style.opacity = target_opacity;
        }, 200);
    }

    else if (clicked) {
        setTimeout(e => {
            warn_window.style.display = "none";
            warn_window.style.opacity = target_opacity;
        }, 200);
    }

    clicked = !clicked;
}


function RegisterHandlers(elements) {
    for (warn in elements) {
        try {
            elements[warn].addEventListener("click", ChangeVisibilityWarnClick);
        } catch {}
    }
}

RegisterHandlers(document.getElementsByClassName("warnings"));
