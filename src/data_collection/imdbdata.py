
import spacy
import neuralcoref
import imdbAPIManager
from processing import dataprocessing
import argparse
import requests
import json
import CONSTANTS
import array as arr

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", type=str, required=True,
    help="path to ml data folder which is processed")
ap.add_argument("-t", "--temp", type=str, required=True,
    help="path to tv or series data folder unprocessed")

args = vars(ap.parse_args())

def process_data(film_id, processing):

    f = open(args['temp'] + '/' + str(film_id) + ".txt")
    data = f.read()
    
    doc = processing.process_data(data)


    w = open(args['data'] + '/' + str(film_id) + ".txt", 'w')

    w.write(doc)

def process_initial_data(film_ids, processing):


    for film_id in film_ids:
        
        film_data = imdbAPIManager.get_synopses(film_id)
        if len(film_data) > 0:
            save_data_in_file(args['temp'] + '/' + str(film_id) + ".txt", film_data)
            process_data(film_id, processing)


def process_film_data(film_id, processing):

    film_data = imdbAPIManager.get_synopses(film_id)

    if len(film_data) > 0:
        save_data_in_file(args['temp'] + '/' + film_id + '.txt', film_data)
        process_data(film_id, processing)

def process_tv_show_data(tv_show_id, processing):

    seasons = imdbAPIManager.get_seasons(tv_show_id)
    w = open(args['temp'] + '/' + str(tv_show_id) + ".txt", 'w')
    for season in seasons:
        for episode_id in season:

            w.write(imdbAPIManager.get_synopses(episode_id))
    
    process_data(tv_show_id, processing)

def retreive_data(imdb_id):

    seasons = imdbAPIManager.get_seasons(imdb_id)

    if (seasons is None) or (len(seasons) == 0):
        process_film_data(imdb_id)
    else:
        process_tv_show_data(imdb_id)

def retrieve_test_data(film_ids, processing):

    for film_id in film_ids:

        text = imdbAPIManager.get_plots(film_id)
        if len(text) > 0:
            save_data_in_file(args['temp'] + '/' + film_id + '.txt', text)

def save_data_in_file(file, data):

    w = open(file, 'w')
    w.write(data)

if __name__ == "__main__":

    processing = dataprocessing()

    film_ids = imdbAPIManager.get_top_movies()

    process_initial_data(film_ids, processing)