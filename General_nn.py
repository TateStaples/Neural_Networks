import simple_neural_network as activations
from copy import deepcopy


class Neuron:
    def __init__(self, network, bias):
        self.bias = bias
        self.value = self.bias
        self.connections = {}
        self.network = network

    def reset(self):
        self.value = self.bias

    def break_connection(self, n):
        self.connections.pop(n)

    def add_connection(self, neuron, weight=1, activation=activations.NeuralNetwork.relu):
        self.connections[neuron] = (weight, activation)

    def fire(self):
        for neuron in self.connections:
            w, a = self.connections[neuron]
            neuron.value += a(self.value) * w
            self.network.append(neuron)
        self.reset()


class Network:
    def __init__(self):
        self.next_to_activate = []

    def add_neuron(self, connections=(), bias=0):
        n = Neuron(self, bias)
        for c in connections:
            n.add_connection(*c)
    
    def run(self):
        while len(self.next_to_activate) > 0:
            next = deepcopy(self.next_to_activate)
            for neuron in next:
                neuron.fire()
            del next
