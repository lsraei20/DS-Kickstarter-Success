import string
import joblib
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import dill
import nltk

nltk.download('stopwords')
model = dill.load(open('/Users/israel/PycharmProjects/'
                       'kickstarter-success-rate/app/'
                       'api/lrm_model.pkl', 'rb'))
model = joblib.load('/Users/israel/PycharmProjects/'
                    'kickstarter-success-rate/app/'
                    'api/lrm_model.pkl')
print((model.predict(["whats up"]))[0])


# PICKLE MODEL 1
def load_pickle(df):
    nltk.download('stopwords')
    model = dill.load(open('/Users/israel/PycharmProjects/'
                           'kickstarter-success-rate/app/'
                           'api/lrm_model.pkl', 'rb'))
    return model.predict([df])


print(load_pickle("hello world"))


# PICKLE MODEL 2
punctuations = string.punctuation
parser = English()
stop_words = spacy.lang.en.stop_words.STOP_WORDS
nltk.download('stopwords')
model = dill.load(open('/Users/israel/PycharmProjects/'
                       'kickstarter-success-rate/app/'
                       'api/dill_pickle_model2.pkl', 'rb'))

print(model.predict(["hello world"]))
