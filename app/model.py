import pandas as pd 
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import re
import string
import random


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin
from sklearn.metrics import accuracy_score, recall_score, plot_confusion_matrix
#from wordcloud import WordCloud
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

from xgboost import XGBClassifier


import warnings

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from sklearn.impute import SimpleImputer
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from pathlib import Path

import joblib


#--------------Cleaning begins -------------------#
BASE_DIR = Path(__file__).resolve(strict=True).parent

#training data
def train():
    df = pd.read_csv('data\kickstarter_data_with_features.csv',index_col=0)
    df = df[['name', 'goal', 'blurb', 'launched_at', 'deadline','category','state', 'country']] 
    english_countries = ['US', 'IE', 'GB', 'AU', 'CA', 'NZ', ]
    df= df[df['country'].isin(english_countries)]
    suc_filt = ['failed', 'successful']
    df= df[df['state'].isin(suc_filt)]
    df['state'] = df['state'].replace({'failed': 0, 'successful': 1})

    columns = ['name','blurb', 'state']
    to_df = df.copy()
    to_df = to_df[columns]  
    to_df.fillna(' ', inplace=True)
    to_df['text']=to_df['name']+' '+to_df['blurb']

   
    punctuations = string.punctuation
    stop_words = spacy.lang.en.stop_words.STOP_WORDS
    parser = English()
    def spacy_tokenizer(sentence):

        mytokens = parser(sentence)
        mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
        mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]
        return mytokens
    # Custom transformer using spaCy
    class predictors(TransformerMixin):
        def transform(self, X, **transform_params):
            
            return [clean_text(text) for text in X]

        def fit(self, X, y=None, **fit_params):
            return self

        def get_params(self, deep=True):
            return {}

    def clean_text(text):
        # Removing spaces and converting text into lowercase
        return text.strip().lower()
    bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,3))

    train, test = train_test_split(to_df, train_size=0.80, test_size=0.20, 
                                stratify= to_df['state'], random_state=3)

    train, val = train_test_split(train, train_size=0.80, test_size=0.20, 
                                stratify= train['state'], random_state=3)
    features = 'text'
    target = 'state'
    X_train = train[features]
    X_val = val[features]
    X_test = test[features]
    y_train = train[target]
    y_val = val[target]
    y_test = test[target]
    xgm = XGBClassifier(n_jobs=-1, max_depth=200, learning_rate=0.2, min_child_weight=5, )

    # Create pipeline using Bag of Words
    pipe = Pipeline([("cleaner", predictors()),
                    ('vectorizer', bow_vector),
                    ('classifier', xgm)])

    # fitting our model.
    pipe.fit(X_train,y_train)
    joblib.dump(pipe, Path(BASE_DIR).joinpath(f"mod.joblib"))
    print("hello!")

train()