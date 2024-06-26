# -*- coding: utf-8 -*-
"""LSTM-Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K7s8J7dHyttqZTMhCoo4V9TAGXEYpeHb

##Reading the file for the processing the data
"""

# The file is uploaded as 'LSTM Data.txt'
with open('LSTM_DATA.txt', encoding='utf-8') as file:
    data = file.read()

# Print the first 500 characters of the data
print(data[:500])

"""##Importing Necessary Libraries"""

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding,Dense,LSTM, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import pickle
import numpy as np
import os

"""###Preprocessing the textual data by tokenizing and generating sequences"""

# The 'data' is the input text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
seqence_data = tokenizer.texts_to_sequences([data])[0]

# Saving the tokenizer
with open('token.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

# Printing the first 15 elements of the sequence data
print(seqence_data[:15])

"""###len(seqence_data) tells us how many items are in the list called seqence_data.

"""

len(seqence_data) # seqence_data is a list of words or tokens

"""###tokenizer.word_index is a part of the Tokenizer object that contains a dictionary. In this dictionary, each unique word from your text data is paired with a number. This number represents the word's index or position in the tokenizer's vocabulary."""

vocab_size = len(tokenizer.word_index) #len(tokenizer.word_index) counts how many unique words (or tokens) are in the text data.
vocab_size #vocab_size is just a number that tells you how many different words are in your text data.

"""###This code takes a list of words (seqence_data) and creates sequences of four consecutive words. It then prints the number of sequences created and the first 10 sequences. NumPy is used to handle the data efficiently."""

import numpy as np # Numerical computation

sequence = [] # initializes an empty list named sequence. This list will be used to store sequences of words.
for i in range(3, len(seqence_data)): # iterates through the seqence_data list starting from the index 3. seqence_data contains sequences of words, and this loop is used to create new sequences with four words each.
    words = seqence_data[i-3:i+1] # This creates a sliding window of four consecutive words.
    sequence.append(words) # adds each sequence of four words to the sequence list.

print('The Length of sequence is:', len(sequence)) # prints the length of the sequence list.
sequence = np.array(sequence) # converts the list of sequences into a NumPy array
print(sequence[:10]) #  Prints the first 10 sequences from the sequence array.

x = [] # creates an empty list named x.
y = [] # creates another empty list named y.
for i in sequence: # iterates through each sequence in the sequence list
    x.append(i[0:3]) # takes the first three elements of the current sequence i and adds them to the x list. This creates a new list of sequences, each containing the first three words.
    y.append(i[3]) # takes the fourth element of the current sequence i and adds it to the y list. This creates a new list of single words, each corresponding to the next word after the first three in each sequence.

x = np.array(x) # converts the list of sequences x into a NumPy array.
y = np.array(y) # converts the list of single words y into a NumPy array.

print(x.shape) # prints the shape of the NumPy array x
print(y.shape) # prints the shape of the NumPy array y

"""###Convert the numerical labels in array y into one-hot encoded vectors."""

y = to_categorical(y,num_classes=7560)

"""##Splitting the data:"""

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=.1)

"""##Building the model"""

model = Sequential()
model.add(Embedding(7560, 10,  input_length=3))
model.add(LSTM(1000,return_sequences=True))
model.add(LSTM(1000))
model.add(Dense(1000, activation='relu'))
model.add(Dense(7560, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',optimizer=Adam(learning_rate=0.001),metrics=['accuracy'])

history = model.fit(xtrain,ytrain,validation_data=(xtest,ytest),epochs=100)

"""##Predict Next Words Model

"""

from tensorflow.keras.preprocessing.sequence import pad_sequences
import time
text = "To some the delightful freshness and humour"

for i in range(15):
  # tokenize
  token_text = tokenizer.texts_to_sequences([text])[0]
  # padding
  padded_token_text = pad_sequences([token_text], maxlen=3, padding='pre')
  # predict
  pos = np.argmax(model.predict(padded_token_text))

  for word,index in tokenizer.word_index.items():
    if index == pos:
      text = text + " " + word
      print(text)
      time.sleep(2)