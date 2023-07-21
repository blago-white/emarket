function SetRange(event) {
    let url = new URL(document.location.href);

    const new_arg_name = event.target.parentElement.id == "max-interval" ? "max" : "min"
    url.searchParams.set(new_arg_name, event.target.value);

    url.searchParams.set("page", "1");
    url.searchParams.set("filters", "1")

    document.location.href = url.href;
}

const input_min = document.getElementById("min-interval-input");
const input_max = document.getElementById("max-interval-input");
input_min.addEventListener("click", SetRange);
input_max.addEventListener("click", SetRange);
input_min.addEventListener("touch", SetRange);
input_max.addEventListener("touch", SetRange);