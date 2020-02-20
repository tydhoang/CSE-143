# @author Tyler Hoang
# CSE 143

# -*- coding: utf-8 -*-
"""A2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q_8DoJUDudIeCF1WJu6ROAc61vp3WyPZ

**Chapter 16 – Natural Language Processing with RNNs and Attention**

_This notebook contains all the sample code in chapter 16._

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/jflanigan/handson-ml2/blob/master/16_nlp_with_rnns_and_attention.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
</table>

# Setup

First, let's import a few common modules, ensure MatplotLib plots figures inline and prepare a function to save the figures. We also check that Python 3.5 or later is installed (although Python 2.x may work, it is deprecated so we strongly recommend you use Python 3 instead), as well as Scikit-Learn ≥0.20 and TensorFlow ≥2.0.
"""

# Commented out IPython magic to ensure Python compatibility.
# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

# TensorFlow ≥2.0 is required
import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"

# Common imports
import numpy as np
import os

# to make this notebook's output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

"""# Sentiment Analysis"""

tf.random.set_seed(42)

"""You can load the IMDB dataset easily:"""

import tensorflow_datasets as tfds

(train_data, validation_data, test_data), info = tfds.load("imdb_reviews", 
                                                                   split=('train[:80%]', 'train[80%:]', 'test'), 
                                                                   as_supervised=True, 
                                                                   with_info=True)

def preprocess(X_batch, y_batch):
    X_batch = tf.strings.substr(X_batch, 0, 300)
    X_batch = tf.strings.regex_replace(X_batch, rb"<br\s*/?>", b" ")
    X_batch = tf.strings.regex_replace(X_batch, b"[^a-zA-Z']", b" ")
    X_batch = tf.strings.split(X_batch)
    return X_batch.to_tensor(default_value=b"<pad>"), y_batch

batch_size=32

from collections import Counter

vocabulary = Counter()
for X_batch, y_batch in train_data.batch(batch_size).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

for X_batch, y_batch in validation_data.batch(batch_size).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

for X_batch, y_batch in test_data.batch(batch_size).map(preprocess):
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

train_set = train_data.batch(batch_size).map(preprocess)
train_set = train_set.map(encode_words).prefetch(1)

validation_set = validation_data.batch(batch_size).map(preprocess)
validation_set = validation_set.map(encode_words).prefetch(1)

test_set = test_data.batch(batch_size).map(preprocess)
test_set = test_set.map(encode_words).prefetch(1)

embed_size = 128
model = keras.models.Sequential([
    keras.layers.Embedding(vocab_size + num_oov_buckets, embed_size,
                           mask_zero=True, # not shown in the book
                           input_shape=[None]),
    keras.layers.LSTM(128, dropout=0.5),
    keras.layers.Dense(1, activation="softplus")
])
model.summary()
model.compile(loss="binary_crossentropy", optimizer="nadam", metrics=["accuracy"])
history = model.fit(train_set, epochs=3, validation_data=validation_set, verbose=1)