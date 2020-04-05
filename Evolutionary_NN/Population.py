from simple_neural_network import *
from copy import deepcopy
import random


# a group of neural networks
class Population:
    def __init__(self, amount, layers, activations=(), mutation_rate=.1, survival_rate=.5):
        self.survival_rate = survival_rate
        self.mutation_rate = mutation_rate
        self.population = []
        self.size = amount
        for i in range(amount):
            net = NeuralNetwork(layers, activations)
            self.population.append(net)

    def play_generation(self, scores, high_bad=False):
        # score_dict = {net: score for net, score in zip(self.population, scores)}
        self.sort_population(scores)
        self.population = self.population[::-1] if not high_bad else self.population
        self.population = self.population[:int(len(self.population)*self.survival_rate)]  # this is the culling - remove bottom half
        self.repopulate()

    def sort_population(self, values):  # todo: change for quicksort
        sorted = []
        sorted_vals = []
        for net, val in zip(self.population, values):
            insertion = self.binary_search(sorted_vals, val)
            sorted.insert(insertion, net)
            sorted_vals.insert(insertion, val)
        self.population = sorted

    def repopulate(self):
        #best_net = deepcopy(self.population[0])
        #self.population = [self.mutate(net) for net in self.population]
        #self.population.insert(0, best_net)
        new_nets = []
        while len(self.population) + len(new_nets) < self.size:
            new_nets.append(self.mutate_merge(random.choice(self.population), random.choice(self.population)))
        self.population.extend(new_nets)

    def mutate_merge(self, net1, net2):
        new_network = []
        for layer1, layer2 in zip(net1.network, net2.network):
            new_layer = []
            for neuron1, neuron2 in zip(layer1, layer2):
                new_weights = []
                for weight1, weight2 in zip(neuron1.weights, neuron2.weights):
                    new_weight = random.choice([weight1, weight2])
                    delta = new_weight * self.mutation_rate
                    new_weight += random.uniform(-delta, delta)
                    new_weights.append(new_weight)
                new_layer.append(Neuron(new_weights))
            new_network.append(new_layer)
        new_net = NeuralNetwork((1, 1))
        new_net.network = new_network
        new_net.activations = net1.activations
        return new_net

    @staticmethod
    def merge(net1, net2):
        new_network = []
        for layer1, layer2 in zip(net1.network, net2.network):
            new_layer = []
            for neuron1, neuron2 in zip(layer1, layer2):
                new_weights = []
                for weight1, weight2 in zip(neuron1.weights, neuron2.weights):
                    average_weight = (weight1 + weight2) / 2
                    new_weights.append(average_weight)
                new_layer.append(Neuron(new_weights))
            new_network.append(new_layer)
        new_net = NeuralNetwork((1, 1), net1.activations)
        new_net.network = new_network
        return new_net

    def mutate(self, net):
        for layer in net.network:
            for neuron in layer:
                new_weights = []
                for weight in neuron.weights:
                    delta = weight * self.mutation_rate
                    weight += random.uniform(-delta, delta)
                    new_weights.append(weight)
                neuron.weights = new_weights
        return net

    @staticmethod
    def binary_search(compare_list, val):
        if len(compare_list) == 0:
            return 0
        low_index = 0
        high_index = len(compare_list) - 1
        while low_index <= high_index:
            middle_index = round((high_index + low_index) / 2)
            if compare_list[middle_index] == val:
                return middle_index
            if val > compare_list[middle_index]:
                low_index = middle_index + 1
            elif val < compare_list[middle_index]:
                high_index = middle_index - 1
        return low_index


if __name__ == '__main__':
    test_list = [1, 2, 5, 9]
    print(test_list[2:])