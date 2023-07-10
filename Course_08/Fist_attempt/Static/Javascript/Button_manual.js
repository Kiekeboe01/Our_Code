function toggleText(elementId, arrowId) {
    /*
    Toggle the text if the button is clicked and change the arrow.
     */
    var x = document.getElementById(elementId);
    var arrow = document.getElementById(arrowId + 'Arrow');
    if (x.style.display === "block") {
        x.style.display = "none";
        arrow.innerHTML = "&darr;"; // Update arrow content to down arrow
    } else {
        x.style.display = "block";
        arrow.innerHTML = "&uarr;"; // Update arrow content to up arrow
    }
}