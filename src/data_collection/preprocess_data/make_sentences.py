import glob
import re
from re import sub
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')

stops = set(stopwords.words('english'))

def remove_punctuations(text):

    punct = ['.', ',', '(', ';', '?', '!', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '%', '&', '*', '@', ':', '-', '_']

    for exp in punct:

        text = text.replace(exp, '')
    


    line = text.split()

    text = ''

    for t in line:
        
        if len(t) < 2:
            continue
            
        text += t + ' '

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


line = "the date is september'th    shortly after the end of world war ii"

def process_text(text):
    
    text = text.replace('\r\n', '.')
    text = text.replace('\n', '.')
    text = text.replace('\r', '.')
    text = text.lower()
    text = text.strip().split('.')

    return text


def write_sentences(filename, text):

    f = open('sentence_labels/' + filename, 'w')
    for line in text:
                
        if line == ' ' or len(line) == 0:
            continue

        line = clean_text(line)
        line = remove_punctuations(line)
        line = line.strip()
        if len(line) < 7:
            continue
        f.write(line + '\n')

for filename in glob.glob('spoilerBlocker/src/data_collection/data/*.txt'):

    f = open(filename, 'r')
    
    text = f.read()

    text = process_text(text)

    write_sentences(filename[filename.find('\\') + 1:], text)

    print('processed    ')