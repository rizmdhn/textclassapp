import pandas as pd
import re
import numpy as np
import sys
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from skmultilearn.problem_transform import LabelPowerset
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  

# Load the RFDT model from the saved pickle file
rfdt_predict_train = joblib.load('public/model_rfdt.pkl')
df = pd.read_csv('public/preproccesed4_dataset.csv', encoding ='ISO-8859-1')
label = ['Ujaran Kebencian', 'Kata Kasar','Individual', 'Group',
       'Agama', 'Ras', 'Tubuh', 'Jenis Kelamin', 'Lainnya',
       'Kategori Ringan', 'Kategori Sedang', 'Kategori Tinggi']

text = sys.argv[1]
def clean_text(text):
  # Convert the text to lowercase
  text = text.lower()
      
  # Remove any URLs from the text
  text = re.sub(r'http\S+', '', text)
  
  # Remove the set of text
  text = re.sub(r'user', '',text)
  text = re.sub(r'rt','',text)
  # Remove any non-alphabetic characters from the text
  text = re.sub(r'[^a-z ]', '', text)
      
  # Remove any extra spaces from the text
  text = re.sub(r'\s+', ' ', text)
      
  # Return the cleaned text
  return text.strip()
final = []
def checkarraynull(array):
  for x in range((predictions.shape[0])):
      t = predictions[x]
      if all(v == 0 for v in t):
        continue
      else :
        final.append(t.tolist())
  return final
def get_result_class(array):
  sum = [0,0,0,0,0,0,0,0,0,0,0,0]
  labels = []
  if len(array) > 1:
    for f in array:
      for i in range(len(f)):
        if f[i] == 1:
          sum[i] += 1
    for i in range(len(sum)):
      quorum = (len(array) / 2) + 1
      if sum[i] >= quorum:
        labels.append(label[i])
  elif len(array) == 1:
    for f in final:
        for i in range(len(f)):
          if f[i] == 1:
            labels.append(label[i])
  elif len(array) == 0:
    labels.append("Tidak ada label")
  return labels
text = clean_text(text)
text = word_tokenize(text)
stopwords = set(sw.words('indonesian'))
filtered_sentence = [w for w in text if not w.lower() in stopwords]
factory = StemmerFactory()
stemmer = factory.create_stemmer()
filtered_sentence = [stemmer.stem(word) for word in filtered_sentence]
tfidf = TfidfVectorizer()
tfidf.fit(df['stemmed_tokens'])
text = tfidf.transform(filtered_sentence).toarray()
# Perform some example predictions
predictions = rfdt_predict_train.predict(text)
predictions = predictions.toarray()
# # Print the predictions
checkarraynull(predictions)
result = get_result_class(final)
print(result, end="")