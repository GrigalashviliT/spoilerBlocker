console.log("if you read this in console spoilerBlocker extension works")

var searchForm = document.querySelector('.search-form')
var searchInput = document.querySelector('.search-input')
var closeButton = document.querySelector('.close-button')
var pauseButton = document.querySelector('#pause')

var storedFilms = {}
var storedFilmsString = localStorage.getItem('stored-films')
if(storedFilmsString != null) {
    storedFilms = JSON.parse(storedFilmsString)
}

var isPaused = localStorage.getItem('isPaused')
if(isPaused == 'true') {
    $('#pause').prop('checked', true)
}

updateBlockedFilms()

function updateBlockedFilms() {
    $('.blocked-films-list').empty()
    for (const [key, value] of Object.entries(storedFilms)) {
        $('.blocked-films-list').append(`<li><i class=blocked-film-title>` + value + `</i><b class='remove-button' onClick='removeFilm(this)' value=` + key + `>x</blocked-film-title></li>`)
    }
}

searchInput.addEventListener('click', () => {
    $('.start-pause-button').hide(1100)
});

pauseButton.addEventListener('click', () => {
    var isPaused = localStorage.getItem('isPaused')

    if (isPaused == null) {
        localStorage.setItem('isPaused', 'true')
    } else if (isPaused == 'true') {
        localStorage.setItem('isPaused', 'false')
    } else {
        localStorage.setItem('isPaused', 'true')
    }
});

closeButton.addEventListener('click', () => {
    searchInput.value = '';
    $('.found-films').empty()
    $('.loading-circle').hide()
    $('.blocked-films').show()
    $('.start-pause-button').show(1100)
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
    console.log(filmId)
    storedFilms[filmId] = filmTitle
    localStorage.setItem('stored-films', JSON.stringify(storedFilms));
    searchInput.value = '';
    $('.found-films').empty()
    $('.blocked-films').show()
    $('.start-pause-button').show(1100)
    updateBlockedFilms()
}

function removeFilm(element) {
    var filmId =  element.attributes.value.value
    console.log(filmId)
    delete(storedFilms[filmId])
    localStorage.setItem('stored-films', JSON.stringify(storedFilms))
    updateBlockedFilms()
}