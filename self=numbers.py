# this is a mnist number set using own
# mid-january
__author__ = "Tate Staples"


import matplotlib.pyplot as plt
from tensorflow import keras
from simple_neural_network import *
import numpy as np

image_number = 3
data = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = data.load_data()


def convert_label(labels):
    new_labels = []
    for label in labels:
        blank = [0 for i in range(10)]
        blank[label] = 1
        new_labels.append(blank)
    return new_labels

train_labels = convert_label(train_labels)
test_labels = convert_label(test_labels)
train_images = [flatten(nump_array.tolist()) for nump_array in train_images]
test_images = [flatten(nump_array.tolist()) for nump_array in test_images]

layers = (784, 100, 10)
activations = NeuralNetwork.relu, NeuralNetwork.sigmoid
net = NeuralNetwork(layers, activations)
print(type(train_images[0]))
net.train_network(train_images, train_labels, 0.1, 1)
net.evaluate(test_images,test_labels)

if __name__ == '__main__':
    pass
