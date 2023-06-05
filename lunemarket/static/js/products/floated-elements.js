const content_card = document.getElementsByClassName('card-info')[0];

const motionMatchMedia = window.matchMedia('(prefers-reduced-motion)');
const threshold_photo = 7;
const threshold_content = 10;

let current_threshold;

function handleHoverContentCard(e) {
    const { clientX, clientY, currentTarget } = e;
    const { clientWidth, clientHeight, offsetLeft, offsetTop } = currentTarget;

    const horizontal = (clientX - offsetLeft) / clientWidth;
    const vertical = (clientY - offsetTop) / clientHeight;
    const rotateX = (threshold_content / 2 - horizontal * threshold_content).toFixed(2);
    const rotateY = (vertical * threshold_content - threshold_content / 2).toFixed(2);

    content_card.style.transform = `perspective(${clientWidth}px) rotateX(${rotateY}deg) rotateY(${rotateX}deg) scale3d(1.05, 1.05, 1.05)`;
}

function resetStylesContentCard(e) {
    content_card.style.transform = `perspective(${e.currentTarget.clientWidth}px) rotateX(0deg) rotateY(0deg)`;
}

if (!motionMatchMedia.matches) {
    content_card.addEventListener('mousemove', handleHoverContentCard);
    content_card.addEventListener('mouseleave', resetStylesContentCard);
}
