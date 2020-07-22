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


async function  spoilerCheck(sent){
    console.log(sent)
    a = await fetch("http://35.233.124.206:5005/model/parse/batch", {
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
        },
        method: "POST",
        body: JSON.stringify({sentences: sent})
    }).then(response => response.json());

    return a
}

async function blockSpoilers() {
    var textOnTab = document.body.innerText
    sentences = textOnTab.split('\n')

    for(var i = checkedSentences / 50; i < sentences.length / 50; i++) {
        var isSpoiler = await spoilerCheck(sentences.slice(i * 50, 50 * (i + 1)))

        for(var k = 0; k < isSpoiler.length; k++) {
            if(isSpoiler[k].confidence > 0.60) {
                var xpath = `//text()[. = '` + sentences[checkedSentences + k] + `']`
                var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
                if (matchingElement != null) {
                    matchingElement.parentNode.innerHTML = warningHTML
                }
            }
        
        }
        console.log('processed')

    }
    checkedSentences += 50

    // for(var i = 0; i < sentences.length; i++) {
    //     console.log(isSpoiler[i], sentences[i])
    // }

    // var sentencesToCheck = sentences.length - checkedSentences
    // for(var i = 0; i < sentencesToCheck; i++) {
    //     if(isSpoiler[i]) {
    //         var xpath = `//text()[. = '` + sentences[checkedSentences + i] + `']`
    //         var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
    //         if (matchingElement != null) {
    //             matchingElement.parentNode.innerHTML = warningHTML
    //         }
    //     }
    // }
    // checkedSentences = sentences.length
}