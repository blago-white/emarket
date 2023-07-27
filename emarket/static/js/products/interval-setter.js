const inputMin = document.getElementById("min-interval-input");
const inputMax = document.getElementById("max-interval-input");
const inputValueMin = document.getElementById("input-price-value-min");
const inputValueMax = document.getElementById("input-price-value-max");

function getPriceWithCurrency(value) {
    return value + "$"
}

inputValueMin.textContent = getPriceWithCurrency(inputMin.value);
inputValueMax.textContent = getPriceWithCurrency(inputMax.value);

function SetRange(event) {
    let url = new URL(document.location.href);

    const new_arg_name = event.target.parentElement.id == "max-interval" ? "max" : "min"
    url.searchParams.set(new_arg_name, event.target.value);

    url.searchParams.set("page", "1");
    url.searchParams.set("filters", "1")

    document.location.href = url.href;
}

function SetInputValue(event) {
    const targetLabel = event.target.id == "max-interval-input" ? inputValueMax : inputValueMin;
    targetLabel.textContent = getPriceWithCurrency(event.target.value);
}

inputMin.addEventListener("change", SetRange);
inputMax.addEventListener("change", SetRange);
