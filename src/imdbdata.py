
import spacy
import neuralcoref
import imdbAPIManager

def process_data(film_id):

    nlp = spacy.load('en_core_web_lg')
    neuralcoref.add_to_pipe(nlp)
    
    f = open("temp\in_" + str(film_id) + ".txt")
    data = f.read()
    doc = nlp(data)

    pronouns = ['I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them', 'Mine', 'My', 'Your', 'Yours', 'Its', 'Hers', 'His', 'our', 'ours', 'your', 'yours', 'their', 'theirs']

    for i in range(len(pronouns)):
        pronouns[i] = pronouns[i].lower()

    w = open("data\ml" + str(film_id) + ".txt", 'w')

    for line in doc:

        if str(line).replace("'", '').lower() in pronouns:
            # print(line, line._.coref_clusters)

            if len(line._.coref_clusters) == 0:
                continue
            
            replace = line._.coref_clusters[0][0]

            if str(replace).replace("'", '').lower() in pronouns:
                continue
            
            w.write(str(replace))

        else:

            w.write(str(line) + " ")

    # save_data_in_file("ml\ml" + str(film_id) + ".txt", text)

def process_initial_data(film_ids):

    for film_id in film_ids:
        
        film_data = imdbAPIManager.get_synopses(film_id)
        if len(film_data) > 0:
            save_data_in_file("temp\in_" + str(film_id) + ".txt", film_data)
            process_data(film_id)

def process_film_data(film_id):

    film_data = imdbAPIManager.get_synopses(film_id)

    if len(film_data) > 0:
        save_data_in_file('temp\in_' + film_id + '.txt', film_data)
        process_data(film_id)

def process_tv_show_data(tv_show_id):

    seasons = imdbAPIManager.get_seasons(tv_show_id)
    w = open("temp\in_" + str(tv_show_id) + ".txt", 'w')
    for season in seasons:
        for episode_id in season:

            w.write(imdbAPIManager.get_synopses(episode_id))
    
    process_data(tv_show_id)

def save_data_in_file(file, data):

    w = open(file, 'w')
    w.write(data)

if __name__ == "__main__":
    film_ids = imdbAPIManager.get_top_movies()
    process_initial_data(film_ids)
