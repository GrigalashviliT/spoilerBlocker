import pandas as pd
import glob
from re import sub

dct = {
    'sentence': [],
    'label': []
}

def process_text(text):
    
    text = text.replace('\r\n', '.')
    text = text.replace('\n', '.')
    text = text.replace('\r', '.')
    text = text.lower()
    text = text.strip().split('.')

    return text


def clean_text(text):

    text = str(text)
    text = text.lower()

    # Clean the text
    text = sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = sub(r"what's", "what is ", text)
    text = sub(r"\'s", " ", text)
    text = sub(r"\'ve", " have ", text)
    text = sub(r"can't", "cannot ", text)
    text = sub(r"n't", " not ", text)
    text = sub(r"i'm", "i am ", text)
    text = sub(r"\'re", " are ", text)
    text = sub(r"\'d", " would ", text)
    text = sub(r"\'ll", " will ", text)
    text = sub(r",", " ", text)
    text = sub(r"\.", " ", text)
    text = sub(r"!", " ! ", text)
    text = sub(r"\/", " ", text)
    text = sub(r"\^", " ^ ", text)
    text = sub(r"\+", " + ", text)
    text = sub(r"\-", " - ", text)
    text = sub(r"\=", " = ", text)
    text = sub(r"'", " ", text)
    text = sub(r"(\d+)(k)", r"\g<1>000", text)
    text = sub(r":", " : ", text)
    text = sub(r" e g ", " eg ", text)
    text = sub(r" b g ", " bg ", text)
    text = sub(r" u s ", " american ", text)
    text = sub(r"\0s", "0", text)
    text = sub(r" 9 11 ", "911", text)
    text = sub(r"e - mail", "email", text)
    text = sub(r"j k", "jk", text)
    text = sub(r"\s{2,}", " ", text)

    line = text.split()

    text = ''

    for t in line:
        
        text += t + ' '

    return text[:-1]

for filename in glob.glob('sentence_labels/*.txt'):
    


    f = open(filename, 'r')
    
    text = f.read()

    text = process_text(text)

    filename = filename[filename.find('\\') + 1:]

    for line in text:

        line = clean_text(line)

        if len(line.split()) < 3 or len(line.split()) > 15:
            continue
        

        line = line[:-1]
        line = line.strip()

        dct['sentence'].append(line)
        dct['label'].append(filename[:filename.find('.')])



df = pd.DataFrame(dct)

df.to_csv('data.csv', encoding='utf-8')
