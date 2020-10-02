function toggleContent(contentId) {
    var displayStatus = document.getElementById(contentId);
    if (document.getElementById(contentId).style.display == 'block') {
        document.getElementById(contentId).style.display = 'none';
    } else if (document.getElementById(contentId).style.display == 'none') {
        document.getElementById(contentId).style.display = 'block';
    }
}

function fadeInAnimation() {
    document.body.style.animationName = 'fadeInAnimation';
    document.body.style.animationDuration = '3s'; 
}