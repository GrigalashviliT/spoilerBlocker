
import spacy
import neuralcoref

class dataprocessing:
    """
        dataprocessing class is to process film or serial data
    """

    def __init__(self):
        
        """
            @logic:
                initialization models and etc.
            @param:
        """

        self.nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(self.nlp)
        self.pronouns = ['I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them', 'Mine', 'My', 'Your', 'Yours', 'Its', 'Hers', 'His', 'our', 'ours', 'your', 'yours', 'their', 'theirs']
        self.pronouns = [pronoun.lower() for pronoun in self.pronouns]

    def process_data(self, text):

        """
            @logic:
                processing text, remove pronouns
            @param:
        """

        doc = self.nlp(text)

        processed_text = ''
        
        for line in doc:

            if str(line).replace("'", '').lower() in self.pronouns:
                # print(line, line._.coref_clusters)

                if len(line._.coref_clusters) == 0:
                    continue
                
                replace = line._.coref_clusters[0][0]

                if str(replace).replace("'", '').lower() in self.pronouns:
                    continue
                
                processed_text += str(replace) + ' '
            else:
                processed_text += str(line) + ' '

        return processed_text