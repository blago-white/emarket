function change_blur_photo(event) {
    if (event.type == 'mouseover') {
        let adjacent_element = document.getElementsByClassName('card-photo-wrapper')[0];
        adjacent_element.animate([{filter: 'blur(.05em)'}], {duration: 200, fill: 'forwards'});
    }
    else if (event.type == 'mouseout') {
        let adjacent_element = document.getElementsByClassName('card-photo-wrapper')[0];
        adjacent_element.animate([{filter: 'blur(0em)'}], {duration: 200, fill: 'forwards'});
    }
}

function change_blur_content(event) {
    if (event.type == 'mouseover') {
        let adjacent_element = document.getElementsByClassName('card-info')[0];
        adjacent_element.animate([{filter: 'blur(.05em)'}], {duration: 200, fill: 'forwards'});
    }
    else if (event.type == 'mouseout') {
        let adjacent_element = document.getElementsByClassName('card-info')[0];
        adjacent_element.animate([{filter: 'blur(0em)'}], {duration: 200, fill: 'forwards'});
    }
}


document.getElementsByClassName("card-photo-wrapper")[0].addEventListener('mouseover', change_blur_content)
document.getElementsByClassName("card-photo-wrapper")[0].addEventListener('mouseout', change_blur_content)
document.getElementsByClassName("card-info")[0].addEventListener('mouseover', change_blur_photo)
document.getElementsByClassName("card-info")[0].addEventListener('mouseout', change_blur_photo)
