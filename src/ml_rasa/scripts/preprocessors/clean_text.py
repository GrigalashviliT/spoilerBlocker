from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from re import sub
from typing import Any, List, Text
from functools import reduce
from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message
from rasa.nlu.training_data import TrainingData

class CleanText(Component):

    provides = ["text"]

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None

        for example in training_data.training_examples:
            example.text = self.preprocess(example.text)

            example.set("text", example.text)


    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        message.text = self.preprocess(message.get('text'))

        message.set("text", message.text)

        print(message.text)

    def remove_punctuations(self, text):

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


    def clean_text(self, text):

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

    def preprocess(self, text):

        text = self.clean_text(text)        
        text = self.remove_punctuations(text)

        return text