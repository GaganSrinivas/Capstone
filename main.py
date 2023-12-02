#!/usr/bin/env python
# coding: utf-8

import os
import sys
import copy
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt

from model import get_model
from utills import rearrange, load_data, extract_piece, swap_piece

# Load or train the model
model = get_model()
adam = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

# Load data
base_path = 'data/puzzle_2x2/'
x_val, y_val = load_data(base_path, 'valid')
x_train, y_train = load_data(base_path, 'train')

# Train the model
model.fit(x_train, y_train, batch_size=64,
          epochs=1, validation_data=(x_val, y_val))

# Load test data
x_test, y_test = load_data(base_path, 'test')

# Testing individual image
im = 22
plt.imshow(x_test[im].astype('float64') + 0.5)
plt.show()

inp = tf.expand_dims(extract_piece(x_test[im]), axis=0)
out = model.predict(inp)[0]
out = tf.argmax(out, axis=1)
rearrange(np.array(x_test[im]) + 0.5, out)

# Testing the whole test set
solved = 0
x_test_proc = []

for i in x_test:
    x_test_proc.append(extract_piece(i))

x_test_proc = np.array(x_test_proc)
out = model.predict(x_test_proc)

for i in range(len(out)):
    pos = tf.argmax(out[i], axis=1)
    if list(pos) == list(y_test[i].reshape(cuts * cuts)):
        solved += 1

print("Accuracy on {} samples: {}%".format(
    len(out), round((solved / i) * 100, 2)))

# Correct prediction percentage for each position
all_val = []

for i in range(len(out)):
    pos = tf.argmax(out[i], axis=1)
    val = (pos == y_test[i].reshape(cuts * cuts)).numpy().astype('int')
    all_val.append(val)

all_val = np.array(all_val)
[round(i, 2) for i in (np.sum(all_val, axis=0) / len(out)) * 100]
