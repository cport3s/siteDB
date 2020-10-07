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

function showCredentials() {
    let loginBox = document.getElementsByClassName('loginBox');
    if (loginBox[0].style.display == 'none') {
        loginBox[0].style.display = 'block';
        loginBox[0].style.animationName = 'fadeInAnimation'
        loginBox[0].style.animationDuration = '1s'
    } else {
        loginBox[0].style.animationName = 'fadeOutAnimation'
        loginBox[0].style.animationDuration = '1s'
        loginBox[0].style.display = 'none'
    };
}