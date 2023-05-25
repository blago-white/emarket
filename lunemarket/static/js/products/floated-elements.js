const photo_card = document.getElementsByClassName('card-photo-wrapper')[0];
const content_card = document.getElementsByClassName('card-info')[0];
const motionMatchMedia = window.matchMedia('(prefers-reduced-motion)');
const THRESHOLD = 5;

function CalcTransformByEventInfo(event) {
    const { clientX, clientY, currentTarget } = event;
    const { clientWidth, clientHeight, offsetLeft, offsetTop } = currentTarget;

    const horizontal = (clientX - offsetLeft) / clientWidth;
    const vertical = (clientY - offsetTop) / clientHeight;
    const rotateX = (THRESHOLD / 2 - horizontal * THRESHOLD).toFixed(2);
    const rotateY = (vertical * THRESHOLD - THRESHOLD / 2).toFixed(2);

    return {'horizontal': horizontal, 'vertical': vertical, 'rotateX': rotateX, 'rotateY': rotateY, 'clientWidth': clientWidth}
}

function handleHoverPhotoCard(event) {
    calculated_transforms = CalcTransformByEventInfo(event);
    photo_card.style.transform = `translateZ(22px) perspective(${calculated_transforms['clientWidth']}px) rotateX(${calculated_transforms['rotateY']}deg) rotateY(${calculated_transforms['rotateX']}deg) scale3d(1, 1, 1)`;
}

function handleHoverContentCard(e) {
    calculated_transforms = CalcTransformByEventInfo(event);
    content_card.style.transform = `translateZ(22px) perspective(${calculated_transforms['clientWidth']}px) rotateX(${calculated_transforms['rotateY']}deg) rotateY(${calculated_transforms['rotateX']}deg) scale3d(1, 1, 1)`;
}

function resetStylesPhotoCard(e) {
    photo_card.style.transform = `perspective(${e.currentTarget.clientWidth}px) rotateX(0deg) rotateY(0deg)`;
}

function resetStylesContentCard(e) {
    content_card.style.transform = `perspective(${e.currentTarget.clientWidth}px) rotateX(0deg) rotateY(0deg)`;
}

if (!motionMatchMedia.matches) {
    photo_card.addEventListener('mousemove', handleHoverPhotoCard);
    photo_card.addEventListener('mouseleave', resetStylesPhotoCard);
    content_card.addEventListener('mousemove', handleHoverContentCard);
    content_card.addEventListener('mouseleave', resetStylesContentCard);
}
