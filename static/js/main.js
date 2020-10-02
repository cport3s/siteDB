function toggleContent(contentId) {
    var displayStatus = document.getElementById(contentId);
    if (displayStatus.style.display == 'block') {
        displayStatus.style.display = 'none';
    } else if (displayStatus.style.display == 'none') {
        displayStatus.style.display = 'block';
    }
}

function fadeInAnimation() {
    document.body.style.animationName = 'fadeInAnimation';
    document.body.style.animationDuration = '3s'; 
}