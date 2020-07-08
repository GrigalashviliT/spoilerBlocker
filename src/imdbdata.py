
import spacy
import neuralcoref
import imdbAPIManager

def process_data(film_ids):
    for film_id in film_ids:
        
        lines = imdbAPIManager.get_synopses(film_id)
        nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(nlp)

        doc = nlp(lines)

        doc._.coref_clusters

        # token = doc[-1]
        # token._.in_coref
        # token._.coref_clusters

        # span = doc[-1:]
        # span._.is_coref

        pronouns = ['I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them', 'Mine', 'My', 'Your', 'Yours', 'Its', 'Hers', 'His', 'our', 'ours', 'your', 'yours', 'their', 'theirs']

        for i in range(len(pronouns)):
            pronouns[i] = pronouns[i].lower()

        text = ''

        for line in doc:

            if str(line).replace("'", '').lower() in pronouns:
                # print(line, line._.coref_clusters)

                if len(line._.coref_clusters) == 0:
                    continue
                
                replace = line._.coref_clusters[0][0]

                if str(replace).replace("'", '').lower() in pronouns:
                    continue
                
                text += ' ' + str(replace)

            else:

                text += ' ' + str(line)

        w = open(film_id + '.txt', 'w')

        w.write(text)

if __name__ == "__main__":
    film_ids = imdbAPIManager.get_top_movies()
    process_data(film_ids)
