import numpy

class NeuralNetwork:
    def __init__(self, layers):
        weight_shapes = [(a, b) for a, b in zip(layers[1:], layers[:-1])]  # this finds the dimensions for each layer
        self.layers = layers
        self.weights = [numpy.random.standard_normal(s) for s in weight_shapes]  # this create each of the weights
        print(self.weights[0][2])
        self.biases = [numpy.zeros((s, 1)) for s in layers[1:]]  # create initial biases

    def predict(self, x):
        for weight, bias in zip(self.weights, self.biases):
            x = self.sigmoid(numpy.matmul(weight, x) + bias)
        return x

    def backpropogate(self, output, ideal):
        output_error = ideal - output  # the difference from expected
        output_delta = output_error * self.sigmoid_derivative(output)  # the step that should be taken to rectify

        error = (weight_k * error_j) * self.sigmoid_derivative(output)  # calculate shift between for weight given error of output neuron

    @staticmethod
    def sigmoid(x):  # sigmoid
        return 1 / (1 + numpy.exp(-x))

    @staticmethod
    def sigmoid_derivative(x):  # derivative of sigmoid
        return x * (x - 1)


with numpy.load('Files/mnist.npz') as data:
    training_images = data['training_images']
    training_labels = data['training_labels']


layer_sizes = (3, 3)
x = numpy.array([
    [1],
    [0],
    [0]
])

net = NeuralNetwork(layer_sizes)
prediction = net.predict(x)
print(prediction)


# now I need to learn to backpropagate

# plt.imshow(training_images[0].reshape(28, 28), cmap='gray')
# plt.show()

layer_sizes = (784, 5, 10)
# x = numpy.ones((layer_sizes[0], 1))
net = NeuralNetwork(layer_sizes)
net.print_accuracy(training_images, training_labels)
# prediction = net.predict(training_images)
# print(numpy.argmax(prediction[0]))