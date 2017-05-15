import os

os.system('sudo pip install nltk')
os.system('export CLASSPATH="%your unzip directory%/stanford-postagger-full-2016-10-31"')
os.system('export STANFORD_MODELS="%your unzip directory%/stanford-postagger-full-2016-10-31/models"')


import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('brown')
