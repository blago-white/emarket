const cardInfo = document.getElementsByClassName("card-info-shrink")[0];
const productInfo = document.getElementsByClassName("prod-info-shrink")[0];
const purchaseBlock = document.getElementsByClassName("purchase-on-shrink")[0];
const expandCardInfoImage = document.getElementsByClassName("expand-button-img")[0];

function expandProductInfo() {
    cardInfo.classList.toggle("card-info-shrink");
    productInfo.classList.toggle("prod-info-shrink");
    purchaseBlock.classList.toggle("purchase-on-shrink");
    expandCardInfoImage.classList.toggle("expand-button-img-expanded");
}
