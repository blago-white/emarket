const floatedElement = document.getElementById('floated-element');

const motionMatchMedia = window.matchMedia('(prefers-reduced-motion)');
const threshold_element = 4;

function handleHoverContentCard(e) {
    const { clientX, clientY, currentTarget } = e;
    const { clientWidth, clientHeight, offsetLeft, offsetTop } = currentTarget;

    const horizontal = (clientX - offsetLeft) / clientWidth;
    const vertical = (clientY - offsetTop) / clientHeight;
    const rotateX = (threshold_element / 2 - horizontal * threshold_element).toFixed(2);
    const rotateY = (vertical * threshold_element - threshold_element / 2).toFixed(2);

    floatedElement.style.transform = `perspective(${clientWidth}px) rotateX(${rotateY}deg) rotateY(${rotateX}deg) scale3d(1.1, 1.1, 1.1)`;
}

function resetStylesContentCard(e) {
    floatedElement.style.transform = `perspective(${e.currentTarget.clientWidth}px) rotateX(0deg) rotateY(0deg)`;
}

if (!motionMatchMedia.matches) {
    floatedElement.addEventListener('mousemove', handleHoverContentCard);
    floatedElement.addEventListener('mouseleave', resetStylesContentCard);
}
