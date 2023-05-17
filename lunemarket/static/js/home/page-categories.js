function onhover(elem) {
    try {
        elem.animate([{filter: 'grayscale(0%)'}], {duration: 200, fill: 'forwards'})
    } catch(err) {
    }
}

function onunhover(elem) {
    try {
        elem.animate([{filter: 'grayscale(100%)'}], {duration: 200, fill: 'forwards'})
    } catch(err) {
    }
}
