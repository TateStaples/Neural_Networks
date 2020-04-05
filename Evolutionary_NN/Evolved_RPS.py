from simple_neural_network import NeuralNetwork
from Evolutionary_NN.Population import Population


def check_input(input):
    if input[0] == 1:  # if rock
        return convert("paper")
    if input[1] == 1:  # if paper return scissors
        return convert("scissors")
    if input[2] == 1:  # if scissors return rock
        return convert("rock")
    return None


def convert(input):
    if type(input) == list:
        top = max(input)
        input = input.index(top) + 1
    if input == [1, 0, 0] or input == 1:
        return "rock"
    if input == [0, 1, 0] or input == 2:
        return "paper"
    if input == [0, 0, 1] or input == 3:
        return "scissors"
    if input == "rock":
        return [1, 0, 0]
    if input == "paper":
        return [0, 1, 0]
    if input == "scissors":
        return [0, 0, 1]
    return None


def score(net):
    total_error = 0
    for option in options:
        predicted = net.get_chances(option)
        actual = check_input(option)
        #'''
        for thing1, thing2 in zip(predicted, actual):
            error = abs(thing2 - thing1)
            total_error += error ** 1
        # print(actual, predicted, total_error)
        #'''
        # total_error += 0 if extreme(predicted) == actual else 1
    return total_error


options = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]
answers = [check_input(game) for game in options]

layer_sizes = (3, 3)
amount_of_generations = 200
generation_size = 1000
pop = Population(generation_size, layer_sizes, [NeuralNetwork.sigmoid])
for i in range(amount_of_generations):
    print('generation', i)
    pop.play_generation([score(net) for net in pop.population], high_bad=True)
pop.sort_population([score(net) for net in pop.population])
net = pop.population[0]
play = input("pick a thing (rock, paper, or scissors) ")
prediction = net.get_chances(convert(play))
print([score(net) for net in pop.population])
print(prediction)
print(convert(prediction))

# rock_odds = prediction[0]
# paper_odds = prediction[1]
# scissor_odds = prediction[2]

# ideal_rock_odds, ideal_paper_odds, ideal_scissor_odds = check_input(x)
#'''