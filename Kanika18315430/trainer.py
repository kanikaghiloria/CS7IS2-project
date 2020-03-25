# -*- coding: utf-8 -*-
"""trainer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1arSd24WQSCf3RZoM-OGuyT07Wjyi4rOY
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
from sklearn.model_selection import train_test_split
import sklearn as sk
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.utils import np_utils, print_summary
import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
import pickle
from keras.callbacks import TensorBoard

from matplotlib import pyplot as plt

cnn_checkpoint_path = "/content/drive/My Drive/Colab Notebooks/CS7IS2 - Artificial Intelligence/cnn_model.h5"
features_path = "/content/drive/My Drive/Colab Notebooks/CS7IS2 - Artificial Intelligence/features"
labels_path = "/content/drive/My Drive/Colab Notebooks/CS7IS2 - Artificial Intelligence/labels"
logs_directory_path = "/content/drive/My Drive/Colab Notebooks/CS7IS2 - Artificial Intelligence/logs"
NumberOfClasses = 15

def cnn_model(x, y, classes):
  # classes = 15
  model = Sequential()
  model.add(Conv2D(32, (5, 5), input_shape=(x,y,1), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
  model.add(Conv2D(64, (5, 5), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))

  model.add(Flatten())
  model.add(Dense(512, activation='relu'))
  model.add(Dropout(0.6))
  model.add(Dense(classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  # file_path = "/content/drive/My Drive/Colab Notebooks/CS7IS2 - Artificial Intelligence/Qickdraw.h5"
  checkpoint = ModelCheckpoint(cnn_checkpoint_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
  callbacks_list = [checkpoint]

  return model, callbacks_list

def load_data():
  file = open(features_path,"rb")
  try:
    features = np.array(pickle.load(file))
  finally:
    file.close()

  file1 = open(labels_path, "rb")
  try:
    labels = np.array(pickle.load(file1))
  finally:
    file1.close()

  return features, labels

def augmentData(features, labels):
    features = np.append(features, features[:, :, ::-1], axis=0)
    labels = np.append(labels, -labels, axis=0)
    return features, labels

def preprocessLabels(labels):
  labels = np_utils.to_categorical(labels)
  return labels

features, labels = load_data()
features, labels = sk.utils.shuffle(features, labels)
print ("features.shape: ", features.shape)
print ("labels.shape: ", labels.shape)

labels = preprocessLabels(labels)
print ("labels.shape: ", labels.shape)

train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0, test_size=0.1)

print (train_x.shape)
print (test_x.shape)
print (train_y.shape)
print (test_y.shape)

train_x = train_x.reshape(train_x.shape[0], 28, 28, 1)
test_x = test_x.reshape(test_x.shape[0], 28, 28, 1)
print ("test_x.shape: ", test_x.shape)
print ("train_x.shape: ", train_x.shape)

modelCNN, callbacks_list = cnn_model(28, 28, NumberOfClasses)
print_summary(modelCNN)

modelCNN.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=3, batch_size=64, callbacks=[TensorBoard(log_dir=logs_directory_path)])

modelCNN.save(cnn_checkpoint_path)

cnn_score = modelCNN.evaluate(test_x, test_y, verbose=0)

train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0, test_size=0.1)

# Implementing K-Means
kmeans = KMeans(n_clusters = 5, random_state=0)

kmeans.fit(train_x, train_y)

kmeans_score = kmeans.score(test_x, test_y)

# Random Forrest
classifier = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=0)
classifier.fit(train_x, train_y)

rfc_score = classifier.score(test_x, test_y)

# # Multi-Layer Perceptron (MLP)

# classifier = MLPClassifier(hidden_layer_sizes=784, random_state=0)

# classifier.fit(train_x, train_y)

# mlp_score = classifier.score(test_x, test_y)

print ("CNN Loss: ", cnn_score[0])
print ("CNN Accuracy: ", cnn_score[1])
print ("K-Means score: " , kmeans_score)
print ("Random Forest Classifier Score: ", rfc_score)
# print ("Multi Layer Perceptron Classifier Score: ", mlp_score)