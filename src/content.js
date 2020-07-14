window.addEventListener('DOMContentLoaded', () => {
    checkCurrentContent()
});

window.onscroll = function() {
    checkCurrentContent()
}

var checkedSentences = 0
var warningHTML = `<div style='color: red'>&#9888; Spoiler</div>`

function checkCurrentContent() {
    chrome.storage.sync.get(['isPaused'], function(items) {
        var isPaused = items['isPaused']
        
        if (isPaused) {
            return
        }

        blockSpoilers()
    });
}

function blockSpoilers() {
    var textOnTab = document.body.innerText
    sentences = textOnTab.split('\n')

    // check which sentences are spoilers
    var isSpoiler = []

    var sentencesToCheck = sentences.length - checkedSentences
    for(var i = 0; i < sentencesToCheck; i++) {
        if(isSpoiler[i]) {
            var xpath = `//text()[. = '` + sentences[checkedSentences + i] + `']`
            var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            if (matchingElement != null) {
                matchingElement.parentNode.innerHTML = warningHTML
            }
        }
    }
    checkedSentences = sentences.length
}