import argparse
import requests
import json
import imdbAPIManager
import CONSTANTS

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", type=str, required=True,
    help="path to ml data folder which is processed")
ap.add_argument("-t", "--temp", type=str, required=True,
    help="path to tv or series data folder unprocessed")

args = vars(ap.parse_args())

def test_accuracy(film_ids):
    
    correct_count = 0
    total_count = 0
    for film_id in film_ids:

        # try:
            f = open(args['temp'] + '/' + str(film_id) + ".txt")
            data = {"sentences":f.read().split("\n")}
            print(film_id)
            r = requests.post(CONSTANTS.MODEL_URL, json = data)
            print(len(r.json()))
            print(r.json())
            break
        # except:
            # print("Exception occured while processing where id = " + film_id)

if __name__ == "__main__":

    film_ids = imdbAPIManager.get_top_movies()

    test_accuracy(film_ids)