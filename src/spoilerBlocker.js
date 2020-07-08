console.log("if you read this in console spoilerBlocker extension works")

var searchForm = document.querySelector('#search-form')
var searchInput = document.querySelector('.search-input')
var closeButton = document.querySelector('.close-button')

closeButton.addEventListener('click', () => {
    searchInput.value = '';
    $('.found-films').empty()
    $('.loading-circle').hide()
});

searchForm.addEventListener('submit', () => {
    $('.found-films').empty()
    $('.loading-circle').show()
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
        <li class='found-film'>
            <div class='found-film-view'>
                <img class='film-picture' src="` + film.image.url + `">
                <div class='film-description'>
                    <p class='film-title'>` + film.title + `</p>
                    <p class='film-year'>` + film.year + `</p>
                </div>
            </div>
        </li>`

        $('.found-films').append(element)
    }

    $('.loading-circle').hide()
}