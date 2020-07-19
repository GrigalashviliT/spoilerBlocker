import argparse
import requests
import json
import imdbAPIManager
import CONSTANTS

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--temp", type=str, required=True,
    help="path to ml data folder which is processed")
ap.add_argument("-d", "--statistics", type=str, required=True,
    help="path to statistics folder")

args = vars(ap.parse_args())

def test_accuracy(film_ids):
    
    total_correct_guesses = 0
    total_wrong_guesses = 0
    total_low_confidence = 0
    st = open(args['statistics'] + '/' + "statistics.txt", "w")
    for film_id in film_ids:

        try:
            correct_guesses = 0
            wrong_guesses = 0
            low_confidence = 0
            f = open(args['temp'] + '/' + str(film_id) + ".txt")
            data = str(f.read()).split("\n")
            f.close()
            request_data = {"sentences":data}
            r = requests.post(CONSTANTS.MODEL_URL, json = request_data)
            result = r.json()
            for response in result:
                confidence = response["confidence"]
                guessed_id = response["name"]
                if confidence > 0.5:
                    if guessed_id == film_id:
                        correct_guesses += 1
                        total_correct_guesses += 1
                    else:
                        wrong_guesses += 1
                        total_wrong_guesses += 1
                else:
                    low_confidence += 1
                    total_low_confidence += 1
            st.write(film_id + "  correct_guesses = " + str(correct_guesses) + "  wrong_guesses  =  " + str(wrong_guesses) + 
                               "  total_count  =  " +str(correct_guesses + wrong_guesses) + "  low_confidence = " + str(low_confidence))
            st.write("\n")
        except:
            print("Exception occured while processing where id = " + film_id)
    st.write("total_correct_guesses = " + str(total_correct_guesses) + "  total_wrong_guesses = " + str(total_wrong_guesses) +
             "  total_count = " + str(total_correct_guesses + total_wrong_guesses) + "  total_low_confidence = " + str(total_low_confidence))

if __name__ == "__main__":

    film_ids = imdbAPIManager.get_top_movies()

    test_accuracy(film_ids)