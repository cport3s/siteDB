function toggleContent(contentId) {
    let displayStatus = document.getElementById(contentId);
    if (displayStatus.style.display == 'none') {
        displayStatus.style.display = 'block';
    } else {
        displayStatus.style.display = 'none';
    };
}

function fadeInAnimation() {
    document.body.style.animationName = 'fadeInAnimation';
    document.body.style.animationDuration = '3s'; 
}