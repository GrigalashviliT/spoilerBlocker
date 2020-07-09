import requests 

URL = "https://imdb8.p.rapidapi.com/title"

HEADERS = {
    "x-rapidapi-host": "imdb8.p.rapidapi.com",
    "x-rapidapi-key": "03eafc7bbbmsh3a5622e67154afap1ccb7cjsn000daaa4538f"
}

# get_top_rated_movies:



def get_top_movies():

    result = ['tt1480055', 'tt1668746', 'tt1829962', 'tt1829963', 'tt1829964', 'tt1837862', 'tt1837863', 'tt1837864', 'tt1851398', 'tt1851397',
              'tt1971833', 'tt2069318', 'tt2070135', 'tt2069319', 'tt2074658', 'tt2085238', 'tt2085239', 'tt2085240', 'tt2084342', 'tt2112510',
              'tt2178782', 'tt2178772', 'tt2178802', 'tt2178798', 'tt2178788', 'tt2178812', 'tt2178814', 'tt2178806', 'tt2178784', 'tt2178796',
              'tt2816136', 'tt2832378', 'tt2972426', 'tt2972428', 'tt3060856', 'tt3060910', 'tt3060876', 'tt3060782', 'tt3060858', 'tt3060860']

    r = requests.get(url = URL+str("/get-top-rated-movies"), headers=HEADERS)

    try:
        data = r.json()
        for elem in data:
            film_id = str(elem["id"])
            last_index = len(film_id) - 1
            st = film_id[(film_id.find('/', 1, last_index)) + 1:last_index]
            result.append(st)
    except:
        print("An exception occured")

    return result

def get_synopses(film_id):
    r = requests.get(url = URL+str("/get-synopses"), params={"tconst":film_id}, headers=HEADERS)

    try:
        data = r.json()
        if (data is None) or (len(data) == 0):
            print("null or empty " + film_id)
            return ""
        return data[0]["text"]
    except:
        print(film_id)

    return ""