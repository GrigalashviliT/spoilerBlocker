window.addEventListener('DOMContentLoaded', (event) => {
    checkCurrentContent()
});

window.onscroll = function() {
    checkCurrentContent()
}

var lastSentence = ''

function checkCurrentContent() {
    var textOnTab = document.body.innerText

    console.log(lastSentence)
    if(lastSentence !== '') {
        textOnTab = textOnTab.substr(textOnTab.indexOf(lastSentence))
    }

    sentences = textOnTab.split('\n')
    sentences.forEach(sentence => {
        // check if sentence is spoiler
        var isSpoiler = false

        if (isSpoiler) {
            $(':contains(' + sentence + ')').css('color', 'red')
        }

        lastSentence = sentence
    });
}