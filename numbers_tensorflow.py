import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np

image_number = 3
data = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = data.load_data()
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(train_images, train_labels, epochs=1)
loss, acc = model.evaluate(test_images, test_labels)
print(f"{acc*100}% accuracy")
predictions = model.predict(test_images)
print(predictions[0])
print(np.argmax(predictions[image_number]))
plt.imshow(test_images[image_number].reshape(28, 28), cmap='gray')
plt.show()

if __name__ == '__main__':
    pass