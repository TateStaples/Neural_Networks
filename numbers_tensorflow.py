import matplotlib.pyplot as plt  # to show images
from tensorflow import keras  # library to create network
import numpy as np  # to modify arrays

image_number = 3  # which image of the test images to use as example - can be set to anything 1-10000
data = keras.datasets.mnist  # fetch the number dataset from the library
(train_images, train_labels), (test_images, test_labels) = data.load_data()  # load the training/testing images and answers
model = keras.Sequential([  # general model
    keras.layers.Flatten(input_shape=(28, 28)),  # the input layer - input is a 28x28 image, this flattens that into 784 neurons
    keras.layers.Dense(128, activation="relu"),  # connects this to a small hidden layer
    keras.layers.Dense(10, activation="softmax")  # connects this to an output of 10 numbers (0-9) and normalizes values to between 0 and 1
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])  # does fancy loading
model.fit(train_images, train_labels, epochs=1)  # trains the model by showing the examples 1 time (epoch)
loss, acc = model.evaluate(test_images, test_labels)  # see how accurate the model was on new images (test data)
print(f"{acc*100}% accuracy")  # print out % accuracy
predictions = model.predict(test_images)  # get all of the answers in a list
print(predictions[image_number])  # print how strongly it believes each number for the example
print(np.argmax(predictions[image_number]))  # find the index of the strongest guess for the examples
plt.imshow(test_images[image_number].reshape(28, 28), cmap='gray')  # draw a grayscale image of the examples
plt.show()  # display

if __name__ == '__main__':  # random entry point - not important
    pass