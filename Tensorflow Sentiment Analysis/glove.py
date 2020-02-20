# @author Tyler Hoang
# CSE 143
# glove.py - pretrained word embeddings
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding

# Others
import nltk
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.manifold import TSNE

import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"
import tensorflow_datasets as tfds
# Set the vocabulary size, and load the imdb data with that vocabulary_size:

vocabulary_size = 100000
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.imdb.load_data(path='imdb.npz', num_words = vocabulary_size)

embeddings_index = dict()
f = open('glove.6B/glove.6B.100d.txt')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

word2id = tf.keras.datasets.imdb.get_word_index()   # dictionary from words to integers (the id of the word in the vocab)
id2word = {i: word for word, i in word2id.items()}
embedding_matrix = np.zeros((vocabulary_size, 100))
for word, index in word2id.items():
    #print(word2id)
    if index > vocabulary_size - 1:
        continue
    else:
        embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[index] = embedding_vector

np.random.seed(42)
tf.random.set_seed(42)

"""# Sentiment Analysis"""

tf.random.set_seed(42)

"""You can load the IMDB dataset easily:"""

(train_data, validation_data, test_data), info = tfds.load("imdb_reviews", 
                                                                   split=('train[:80%]', 'train[80%:]', 'test'), 
                                                                   as_supervised=True, 
                                                                   with_info=True)

train_examples_batch, train_labels_batch = next(iter(test_data.batch(10)))
train_examples_batch

def preprocess(X_batch, y_batch):
    X_batch = tf.strings.substr(X_batch, 0, 300)
    X_batch = tf.strings.regex_replace(X_batch, rb"<br\s*/?>", b" ")
    X_batch = tf.strings.regex_replace(X_batch, b"[^a-zA-Z']", b" ")
    X_batch = tf.strings.split(X_batch)
    return X_batch.to_tensor(default_value=b"<pad>"), y_batch

from collections import Counter

vocabulary = Counter()
for X_batch, y_batch in train_data.batch(32).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

for X_batch, y_batch in validation_data.batch(32).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

for X_batch, y_batch in test_data.batch(32).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

vocab_size = 10000
truncated_vocabulary = [
    word for word, count in vocabulary.most_common()[:vocab_size]]

words = tf.constant(truncated_vocabulary)
word_ids = tf.range(len(truncated_vocabulary), dtype=tf.int64)
vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)
num_oov_buckets = 1000
table = tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)

def encode_words(X_batch, y_batch):
    return table.lookup(X_batch), y_batch

train_set = train_data.batch(32).map(preprocess)
train_set = train_set.map(encode_words).prefetch(1)

validation_set = validation_data.batch(32).map(preprocess)
validation_set = validation_set.map(encode_words).prefetch(1)

test_set = test_data.batch(32).map(preprocess)
test_set = test_set.map(encode_words).prefetch(1)


## create model

predict_sentence = np.array([[word2id['the'], word2id['movie'], word2id['will'], word2id['increase'], word2id['my'], word2id['happiness']]])

embed_size = 100
model = keras.models.Sequential([
    keras.layers.Embedding(vocabulary_size, embed_size, weights=[embedding_matrix], trainable=False),
    keras.layers.GRU(128, dropout=0.2),
    keras.layers.Dense(1, activation="softplus")
])
model.summary()
model.compile(loss="binary_crossentropy", optimizer="nadam", metrics=["CosineSimilarity"])
history = model.fit(train_set, epochs=7, validation_data=validation_set, verbose=1)
print(model.predict(predict_sentence))
