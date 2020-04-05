from simple_neural_network import NeuralNetwork


class CovolutionalNN(NeuralNetwork):
    def __init__(self, image, layers):
        self.image = image
        super(CovolutionalNN, self).__init__(0,0)

    def relu_image(self):  # needs a way tp bp
        return [self.relu(pixel) for pixel in self.image]

    def apply_filter(self, filter):
        pass

    def condence(self, image, step):
        pass

    def apply_layer(self, filters):
        return [self.apply_filter(thing) for thing in filters]



