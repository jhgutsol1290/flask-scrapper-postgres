from string import punctuation

import nltk
import spacy
import pandas as pd
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextAnalyzer:
    def __init__(self):
        self.word_list = []
        self.stop_words = []
        self.new_text = []
        self.non_words = []
        self.valid_languages = ['spanish', 'english']
        self.data = None

    def tokenize_words(self, word_list: str, lang: str) -> list:
        if lang not in self.valid_languages:
            lang = 'spanish'
        self.word_list = word_list
        self.new_text = word_tokenize(self.word_list)
        self.remove_punctuation()
        self.filtered_words = [word for word in self.new_text if (
            word not in self.stop_words and word not in self.non_words)]
        self.data = self.stem_text(lang)
        return self.data

    def remove_punctuation(self) -> list:
        self.non_words = list(punctuation)
        self.non_words.extend(['¿', '¡', '...'])
        self.non_words.extend(map(str, range(10)))

    def stem_text(self, lang: str) -> list:
        spanish_stemmer = SnowballStemmer(lang)
        stems = [spanish_stemmer.stem(token) for token in self.filtered_words]
        return stems


class WordFrequency:
    def get_most_frequent_words(self, text: str) -> list:
        self.fdist = nltk.FreqDist(text)
        return self.fdist.most_common(20)

    def get_data(self, text1: list, text2: list) -> float:
        doc1 = ' '.join(text1)
        doc2 = ' '.join(text2)
        train_set = [doc1, doc2]
        tfid_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfid_vectorizer.fit_transform(train_set)
        sim = cosine_similarity(
            tfidf_matrix_train[0:1], tfidf_matrix_train).tolist()
        if sim[0][1] == 0:
            res = 0
        else:
            res = 1 - sim[0][1]
        return res

# class WordsSimilarity:
#     def words_similarity(self, arr1: list, arr2: list) -> float:
#         nlp = spacy.load('es_core_news_sm')
#         doc1 = ' '.join(arr1)
#         doc2 = ' '.join(arr2)
#         doc1 = nlp(doc1)
#         doc2 = nlp(doc2)
#         return doc1.similarity(doc2)
