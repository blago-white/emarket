let bgIsStatic = false;

function HandleCurrentBodySize(event=false) {
    if (document.body.scrollHeight != document.body.offsetHeight) {
        if (!bgIsStatic) {
            SetSimpleBg();
        }
    } else if (bgIsStatic) {
        SetFloatedBg();
    }
}

function SetFloatedBg() {
    const body = document.body;
    body.classList.remove("static-bg");
    bgIsStatic = false;
}

function SetSimpleBg() {
    const body = document.body;
    body.classList.add("static-bg");
    bgIsStatic = true;
}

HandleCurrentBodySize()
window.addEventListener("resize", HandleCurrentBodySize);
