import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer

from keras import Input
from keras.src.callbacks import TensorBoard
import keras.src.saving

import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]

words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)
    
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)

training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]

model = tf.keras.Sequential([
    Input(shape=(len(trainX[0]),)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(trainY[0]), activation='softmax')
])

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1, callbacks=[tensorboard_callback])

# model.save('chatbot_model.h5', hist)
keras.saving.save_model(model, 'chatbot_model.keras')
# model.save('chatbot_model.keras')
with open('training_history.pkl', 'wb') as file:
    pickle.dump(hist.history, file)

print('Model Trained Successfully!')
