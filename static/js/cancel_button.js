const buttonCancel = document.getElementById("buttonCancel")

buttonCancel.addEventListener("click", function () {
    window.history.back();
    return false;
});