from simple_neural_network import NeuralNetwork

def check_input(input):
    if input[0] == 1:  # if rock
        return [0, 1, 0]
    if input[1] == 1:  # if paper return scissors
        return [0, 0, 1]
    if input[2] == 1:  # if scissors return rock
        return [1, 0, 0]
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


layer_sizes = (3, 3)
options = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]
answers = [check_input(game) for game in options]

net = NeuralNetwork(layer_sizes)
net.train_network(options, answers, .3, 300)
with open("Files/RockPaperScissor_trained_net", "w") as file:
    #net.insert_weights_from_file(file)
    net.write_to_file(file)
prediction = net.get_chances(convert("paper"))
print(convert(prediction))

# rock_odds = prediction[0]
# paper_odds = prediction[1]
# scissor_odds = prediction[2]

# ideal_rock_odds, ideal_paper_odds, ideal_scissor_odds = check_input(x)
#'''