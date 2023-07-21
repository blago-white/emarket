const photoSaveButton = document.getElementById("save-photo");
const dropPhotoButtonImg = document.getElementById("drop-file-button-img");
const dropPhotoButtonBgImg = document.getElementById("drop-file-button-img-bg");
const uploadControls = document.getElementById("upload-controls");
const changePhotoLabel = document.getElementById("change-photo-label");

function uploadNewPhoto(event) {
    photoSaveButton.style.display = "flex";
    photoSaveButton.style.display = "flex";

    changePhotoLabel.innerHTML = "uploaded " + "<span style='font-weight: 100;max-width: 14ch;display: inline-flex;overflow: hidden;'>" + event.target.files[0].name + "</span>";

    dropPhotoButtonImg.style.width = "0.6em";
    dropPhotoButtonImg.style.height = "0.6em";
    dropPhotoButtonImg.style.fontSize = "1em";

    dropPhotoButtonBgImg.style.width = "1em";
    dropPhotoButtonBgImg.style.height = "1em";
    dropPhotoButtonBgImg.style.fontSize = "1em";

    uploadControls.style.width = "1em";
    uploadControls.style.height = "1em";
    uploadControls.style.fontSize = "1em";
}