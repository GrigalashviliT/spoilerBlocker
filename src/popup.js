var searchForm = document.querySelector('.search-form')
var searchInput = document.querySelector('.search-input')
var closeButton = document.querySelector('.close-button')
var pauseButton = document.querySelector('#pause')

var storedFilms = {}
chrome.storage.sync.get(['storedFilms'], function(items) {
    var storedFilmsString = items['storedFilms']

    if(storedFilmsString != null) {
        storedFilms = JSON.parse(storedFilmsString)
    }

    updateBlockedFilms()
});

chrome.storage.sync.get(['isPaused'], function(items) {
    var isPaused = items['isPaused']

    if (isPaused) {
        $('#pause').prop('checked', true)
    }
});

function updateBlockedFilms() {
    $('.blocked-films-list').empty()
    for (const [key, value] of Object.entries(storedFilms)) {
        $('.blocked-films-list').append(`<li><i class=blocked-film-title>` + value + `</i><b class='remove-button' onClick='removeFilm(this)' value=` + key + `>x</blocked-film-title></li>`)
    }
}

searchInput.addEventListener('click', () => {
    $('.start-pause-button').hide(1500)
});

pauseButton.addEventListener('click', () => {
    chrome.storage.sync.get(['isPaused'], function(items) {
        var isPaused = items['isPaused']

        if (isPaused) {
            chrome.storage.sync.set({'isPaused': false})
        } else {
            chrome.storage.sync.set({'isPaused': true})
        }
    });
});

closeButton.addEventListener('click', () => {
    searchInput.value = '';
    $('.found-films').empty()
    $('.loading-circle').hide()
    $('.blocked-films').show()
    $('.start-pause-button').show(1500)
});

searchForm.addEventListener('submit', () => {
    $('.found-films').empty()
    $('.loading-circle').show()
    $('.blocked-films').hide()
    searchFilmByTitle();
    event.preventDefault();
});

function searchFilmByTitle() {
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://imdb8.p.rapidapi.com/title/find?q=",
        "method": "GET",
        "success" : function (response) {
            processResponse(response.results)
        },
        "headers": {
            "x-rapidapi-host": "imdb8.p.rapidapi.com",
            "x-rapidapi-key": "03eafc7bbbmsh3a5622e67154afap1ccb7cjsn000daaa4538f"
        }
    }
    
    if(searchInput.value === '')
        return

    settings.url += encodeURIComponent(searchInput.value)
    $.ajax(settings);
};

function processResponse(result) {
    result = result.filter(elm => (elm.titleType == 'movie' || elm.titleType == "tvSeries") && (typeof elm.image !== 'undefined') )

    var size = Math.min(result.length, 3)
    for(i = 0; i < size; i++) {
        var film = result[i]

        var element = `
        <li class='found-film' onClick='addToBlockedFilms(this)'>
            <div class='found-film-view'>
                <img class='film-picture' src=` + film.image.url + `>
                <div class='film-description' value=` + film.id.split('/')[2] + `>
                    <p class='film-title'>` + film.title + `</p>
                    <p class='film-year'>` + film.year + `</p>
                </div>
            </div>
        </li>`

        $('.found-films').append(element)
    }

    $('.loading-circle').hide()
}

function addToBlockedFilms(filmDiv) {
    var filmTitle = filmDiv.children[0].children[1].children[0].textContent
    var filmId = filmDiv.children[0].children[1].attributes.value.value
    storedFilms[filmId] = filmTitle
    chrome.storage.sync.set({'storedFilms': JSON.stringify(storedFilms)})
    searchInput.value = '';
    $('.found-films').empty()
    $('.blocked-films').show()
    $('.start-pause-button').show(1500)
    updateBlockedFilms()
}

function removeFilm(element) {
    var filmId =  element.attributes.value.value
    delete(storedFilms[filmId])
    chrome.storage.sync.set({'storedFilms': JSON.stringify(storedFilms)})
    updateBlockedFilms()
}