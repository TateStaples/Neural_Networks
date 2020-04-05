
from tensorflow import keras
import matplotlib.pyplot as plt
# example of defining the discriminator model
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import LeakyReLU
from keras.utils.vis_utils import plot_model

data = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = data.load_data()


def softmax_255(x, deriv=False):
    if x < 0:
        return 0
    if x <= 255:
        return 1 if deriv else x
    return 0 if deriv else 255

def unflatten(og_list, dimensions=(28, 28)):
    new_list = []
    r, c = dimensions
    for i in range(r):
        new_row = []
        for j in range(c):
            new_row.append(og_list[r*i+j])
        new_list.append(new_row)
    return new_list


data = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = data.load_data()


