import requests 
import CONSTANTS

def get_top_movies():

    result = ['tt0185906', 'tt0306414', 'tt0475784', 'tt0903747', 'tt0944947', 'tt1475582', 'tt1796960', 'tt2356777', 'tt7366338']

    r = requests.get(url = CONSTANTS.URL+str("/get-top-rated-movies"), headers=CONSTANTS.HEADERS)

    try:
        data = r.json()
        for elem in data:
            film_id = str(elem["id"])
            last_index = len(film_id) - 1
            st = film_id[(film_id.find('/', 1, last_index)) + 1:last_index]
            result.append(st)
    except:
        print("An exception Occured in get_top_movies")
    return result

def get_synopses(film_id):
    r = requests.get(url = CONSTANTS.URL+str("/get-synopses"), params={"tconst":film_id}, headers=CONSTANTS.HEADERS)

    try:
        data = r.json()
        if (data is None) or (len(data) == 0):
            return ""
        return data[0]["text"]
    except:
        print("An exception Occured in get_synopses where id = " + film_id)
    return ""

def get_seasons(tv_show_id):
    r = requests.get(url = CONSTANTS.URL+str("/get-seasons"), params={"tconst":tv_show_id}, headers=CONSTANTS.HEADERS)

    try:

        data = r.json()
        seasons = []
        for season in data:

            episode_ids = []
            for episode in season["episodes"]:

                episode_id = episode["id"]
                last_index = len(episode_id) - 1
                imdb_id = episode_id[(episode_id.find('/', 1, last_index)) + 1:last_index]
                episode_ids.append(imdb_id)
            seasons.append(episode_ids)
        return seasons
    except:
        print("An exception Occured in get_seasons whre tv_show_id = " + str(tv_show_id))
    return []

def get_plots(film_id):

    r = requests.get(url = CONSTANTS.URL+str("/get-plots"), params={"tconst":film_id}, headers=CONSTANTS.HEADERS)

    try:

        data = r.json()
        plots = data["plots"]

        text = ""
        for plot in plots:
            text += plot["text"]
            text += '\n'
        return text
    except:
        print("An exception occured in get_plots where film_id = " + film_id)
    return ""