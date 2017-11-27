import re
import pprint
from nltk import word_tokenize, sent_tokenize, pos_tag, RegexpParser
import json
from nltk.stem import WordNetLemmatizer
from nltk.classify import ClassifierI
import pickle
import os
from statistics import mode
from pymongo import *

class OpinionExtractor:
    def __init__(self):
        # self.data_source = json.load(open('data.json','r'))
        self.sentiment_classifier = pickle.load(open("naivebayes.pickle", "rb"))
        self.word_features = pickle.load(open("word_features5k.pickle", "rb"))
        self.lemmatizer = WordNetLemmatizer()
        self.dbclient = MongoClient()
        self.db = self.dbclient['cloud_db']
        
        if os.path.exists('aggregated.json'):
            self.aggregation_data = json.load(open('aggregated.json','rb'))
        else:
            self.aggregation_data ={}

    def find_features(self, document):
        words = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in words)

        return features

    def pos_tag_my(self, text):
        """
        splits a text stream into sentences, tokenizes and returns a list of pos tagged sentences
        """
        word_tokenized = word_tokenize(text)
        lemmatized_sentence = [self.lemmatizer.lemmatize(word) for word in word_tokenized]
        
        return pos_tag(lemmatized_sentence)

    def np_chunk(self, pos_tagged):
        """
        returns the noun phrases in the sentences
        """
        grammar = r"""
        NP: {<DT>?<JJ.*>*<NN.*>+}
        """
        chunk_parser = RegexpParser(grammar)
        # for subtree in tree.subtrees():
            # if subtree.label() == 'CHUNK': print(subtree)
        return [ chunk_parser.parse(sent) for sent in pos_tagged]

    def analyze_sentiment(self, text):
        return self.sentiment_classifier.classify(self.find_features(text))

    def process(self,model):
        data = self.read_data(model)
        self.model = model

        if not(self.aggregation_data.has_key(model)):
            self.aggregation_data[model] = {}
        
        for review in data:
            # sentences = sent_tokenize(review)
            sentences = sent_tokenize(review['comment'])
            for sentence in sentences:
                sentiment = self.analyze_sentiment(sentence)
                pos_tags = self.pos_tag_my(sentence)
                nouns =  self.find_pos_tagged_words(pos_tags, "NN")
                adjectives = self.find_pos_tagged_words(pos_tags, "JJ")
                self.associate_adjectives_nouns(adjectives, nouns)    
                for noun in nouns:
                    self.aggregation_data[model][noun]['sentiment'][sentiment] += 1
        
        json.dump(self.aggregation_data, open('aggregated.json','wb'))

    def read_data(self, model):
        return self.db[model].find()
        # return self.data_source[model]

    def associate_adjectives_nouns(self, adjectives, nouns):
        model = self.model
        for noun in nouns:
            if not(self.aggregation_data[model].has_key(noun)):
                self.aggregation_data[model][noun] = {}
                self.aggregation_data[model][noun]['sentiment'] = {}
                self.aggregation_data[model][noun]['sentiment']['pos'] = 0
                self.aggregation_data[model][noun]['sentiment']['neg'] = 0
                self.aggregation_data[model][noun]['adjectives'] = []
            for adjective in adjectives:
                self.aggregation_data[model][noun]['adjectives'].append(adjective)

    def find_pos_tagged_words(self, tagged_items, tag):
        retval = []
        for tagged_item in tagged_items:
            if tagged_item[1].startswith(tag):
                retval.append(tagged_item[0])
        return retval
