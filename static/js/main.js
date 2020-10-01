function toggleContent(contentClass) {
    let displayStatus = document.getElementById(contentClass);
    console.log(displayStatus.style.display);
    if (displayStatus.style.display == 'block') {
        displayStatus.style.display = 'none';
    } else if (displayStatus.style.display == 'none') {
        displayStatus.style.display = 'block';
    }
}