let clicked = false;


function ChangeVisibilityWarnHover(event) {
    if (clicked) {return}
    console.log(event.type);

    let warn_window;
    const target_element = event.type == "mouseenter" ? event.toElement.id : event.fromElement.id;

    warn_window = document.getElementById(
        "warn-window-" + target_element
    );

    const target_opacity = event.type == "mouseenter" ? "1" : "0";
    warn_window.animate({"opacity": target_opacity}, {duration: 200, easing: "ease-in-out"})

    if (event.type == "mouseenter") {
        warn_window.style.display = "unset";
    }

    else if (event.type == "mouseleave") {
        setTimeout(e => {
            warn_window.style.display = "none"
        }, 200);
    }

    setTimeout(e => {
        warn_window.style.opacity = target_opacity;
    }, 200);
}

function ChangeVisibilityWarnClick(event) {
    clicked = !clicked;
}


function RegisterHandlers(elements) {
    for (warn in elements) {
        try {
            elements[warn].addEventListener("mouseenter", ChangeVisibilityWarnHover);
            elements[warn].addEventListener("mouseleave", ChangeVisibilityWarnHover);
            elements[warn].addEventListener("click", ChangeVisibilityWarnClick);
        } catch {}
    }
}

RegisterHandlers(document.getElementsByClassName("warnings"));
