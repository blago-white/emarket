function card_hover_handler(event) {
    if (event.type == 'mouseover') {
        let cards = document.getElementsByClassName('cards')[0];
        set_grayscale_on_hover(cards);
    }
    if (event.type == 'mouseout' && event.fromElement.parentElement.className != 'card-content') {
        let cards = document.getElementsByClassName('cards')[0];
        unset_grayscale_on_hover(cards);
    }
}

function unset_grayscale_on_hover(elem) {
    try {
        elem.animate([{filter: 'grayscale(0%)'}], {duration: 200, fill: 'forwards'})
    } catch(err) {}
}

function set_grayscale_on_hover(elem) {
    try {
        elem.animate([{filter: 'grayscale(75%)'}], {duration: 200, fill: 'forwards'})
    } catch(err) {}
}


let cards = document.getElementsByClassName("card")
for (card in cards) {
    if (cards[card].className == 'card') {
        cards[card].addEventListener('mouseover', card_hover_handler);
        cards[card].addEventListener('mouseout', card_hover_handler);
    }
}
