window.addEventListener('DOMContentLoaded', () => {
    checkCurrentContent()
});

window.onscroll = function() {
    checkCurrentContent()
}

var checkedSentences = 0
var warningHTML = `<div class='blocked-spoiler'>&#9888; Spoiler</div>`
var batchSize = 20
var threshHold = 0.7

var storedFilms = {}
chrome.storage.sync.get(['storedFilms'], function(items) {
    var storedFilmsString = items['storedFilms']

    if(storedFilmsString != null) {
        storedFilms = JSON.parse(storedFilmsString)
    }
});

function checkCurrentContent() {
    chrome.storage.sync.get(['isPaused'], function(items) {
        var isPaused = items['isPaused']
        if (isPaused) {
            return
        }
        blockSpoilers()
    });
}

async function blockSpoilers() {
    var textOnTab = document.body.innerText
    sentences = textOnTab.split('\n')

    for(var i = checkedSentences / batchSize; i < sentences.length / batchSize; i++) {
        var curSentences = sentences.slice(i * batchSize, (i + 1) * batchSize)
        var isSpoiler = await spoilerCheck(curSentences)

        for(var k = 0; k < isSpoiler.length; k++) {
            if(isSpoiler[k].confidence > threshHold && isSpoiler[k].name in storedFilms) {
                var xpath = `//text()[. = '` + curSentences[k] + `']`
                var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
                if (matchingElement != null) {
                    var previousText = matchingElement.parentNode.innerHTML
                    var newText = warningHTML.substr(0, 37) + storedFilms[isSpoiler[k].name] + warningHTML.substr(36)

                    matchingElement.parentNode.onmouseover = function() {
                        this.innerHTML = previousText
                    }

                    matchingElement.parentNode.onmouseout = function() {
                        this.innerHTML = newText
                    }

                    matchingElement.parentNode.innerHTML = newText   
                }
            }
        }
        checkedSentences += curSentences.length
    }
}

async function spoilerCheck(sent) {
    var result = await fetch("http://35.233.124.206:5005/model/parse/batch", {
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
        },
        method: "POST",
        body: JSON.stringify({sentences: sent})
    }).then(response => response.json())
    return result
}