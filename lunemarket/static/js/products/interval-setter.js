function SetRange(event) {
    let url = new URL(document.location.href);
    url.searchParams.set("min", event.target.value);
    url.searchParams.set("page", "1");
    document.location.href = url.href;
}

const input = document.getElementsByClassName("price-interval")[0];
input.addEventListener("click", SetRange);
