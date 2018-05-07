import re
import csv
import sys
import numpy as np
import pandas as pd
from pprint import pprint
import pickle

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt


# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

data_lemmatized = pickle.load(open('data_lemmatized_all', "rb"))

lda_negative = gensim.models.ldamodel.LdaModel.load('lda_negative', mmap='r')
lda_positive = gensim.models.ldamodel.LdaModel.load('lda_positive', mmap='r')

id2word_negative = corpora.Dictionary.load("lda_negative.id2word")
id2word_positive = corpora.Dictionary.load("lda_positive.id2word")


def get_topic_prob(new_texts, lda_model, id2word, prefix, num_columns=21):
    corpus = [id2word.doc2bow(text) for text in new_texts]
    
    columns = list(range(0,num_columns))
    df_topic_prob = pd.DataFrame(columns=columns)
    for review in corpus:
        topic_prob = [0] * num_columns
        highest_prob = 0
        dominant_topic = 0
        for item in lda_model.get_document_topics(review):
            topic, prob = item[0], item[1]
            topic_prob[topic] = prob
            if prob > highest_prob:
                dominant_topic = topic
                highest_prob = prob
        topic_prob[-1] = dominant_topic
        df_topic_prob = df_topic_prob.append(pd.Series(topic_prob),ignore_index=True)
    for i in range(20):
        df_topic_prob = df_topic_prob.rename(columns = {i: prefix + '_' + str(i)})
    df_topic_prob = df_topic_prob.rename(columns = {20:prefix + '_' + 'dominant_topic'})
    return df_topic_prob



