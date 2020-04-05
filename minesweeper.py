from simple_neural_network import NeuralNetwork
from simple_neural_network import flatten
from random import randint


def get_neighbors(board, r, c, corners=True):
    things = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if not (x == 0 and y == 0):
                try:
                    if not corners and (x != 0 and y != 9):
                        1/0
                    new_r, new_c = r + x, c + y
                    if new_c < 0 or new_r < 0:
                        1/0
                    val = board[new_r][new_c]
                    things.append(((new_r, new_c), val))
                except:
                    pass
    return things


def reveal(board, r, c):
    amount_of_bombs = 0
    for cords, val in get_neighbors(board, r, c):
        if val == 11:
            amount_of_bombs += 1
    board[r][c] = amount_of_bombs
    if amount_of_bombs == 0:
        neighbors = get_neighbors(board, r, c, False)
        for cords, val in neighbors:
            r, c = cords
            if board[r][c] == 10:
                board = reveal(board, r, c)
    return board


def generate_2d(length, width, default_value=None):
    the_list = []
    for i in range(length):
        row = []
        for j in range(width):
            row.append(default_value)
        the_list.append(row)
    return the_list


def extremisize(og_list, top_amount):
    tops = []
    for i in range(top_amount):
        top = max(og_list)
        top_index = og_list.index(top)
        tops.append(top_index)
        og_list[top_index] = 0
    new_list = [0 for i in range(len(og_list))]
    for top in tops:
        new_list[top] = 1
    return new_list


def generate_situation():
    unknown_val = 10
    bomb_val = 11
    dimension = 3
    amount_of_bombs = 2
    amount_revealed = 5
    board = generate_2d(dimension, dimension, unknown_val)
    bomb_map = generate_2d(dimension, dimension, 0)
    bombs = generate_bombs(dimension-1, dimension-1, amount_of_bombs)
    # print(bombs)
    for r, c in bombs:
        # print(r, c)
        board[r][c] = bomb_val
        bomb_map[r][c] = 1
    for r, row in enumerate(board):
        for c, spot in enumerate(row):
            if spot == unknown_val and (r, c) not in bombs:
                board = reveal(board, r, c)
                amount_revealed -= 1
                if amount_revealed == 0:
                    break
        if amount_revealed == 0:
            break
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == bomb_val:
                board[r][c] = unknown_val
    # print(board)
    r = flatten(bomb_map)
    s = flatten(board)
    return r, s


def generate_bombs(r_max, c_max, amount):
    bombs = []
    for i in range(amount):
        r = randint(0, r_max)
        c = randint(0, c_max)
        while (r, c) in bombs:
            r = randint(0, r_max)
            c = randint(0, c_max)
        bombs.append((r, c))
    return bombs


def bomb_generator():
    for first in range(9):
        row1 = int(first // 3)
        col1 = first % 3
        for second in range(9):
            row2 = int(second // 3)
            col2 = second % 3
            if not (row2 == row1 and col2 == col1):
                yield [(row1, row2), (row1, row2)]


def get_accuracy(network, trials):
    correct = 0
    for i in range(trials):
        r, s = generate_situation()
        chances = network.get_chances(s)
        prediction = extremisize(chances, 2)
        if prediction == r:
            correct += 1
    percentage = round(correct/trials * 100, 2)
    print(f"Your net got {correct}/{trials} correct! that is {percentage}%")
    return percentage


if __name__ == '__main__':
    amount_of_data = 400
    situations = []
    results = []
    for i in range(amount_of_data):
        r, s = generate_situation()
        situations.append(s)
        results.append(r)
    print("data created")

    layers = (9, 15, 9)
    activators = (NeuralNetwork.tanh, NeuralNetwork.sigmoid)
    net = NeuralNetwork(layers, activators)
    net.train_network(train_data=situations, train_results=results, l_rate=.9, n_epoch=300, refine_to=.2)
    print("net trained")
    get_accuracy(net, 10000)
    r, s = generate_situation()
    chances = net.get_chances(s)
    prediction = extremisize(chances, 2)
    print()
    print(prediction[0:3])
    print(prediction[3:6])
    print(prediction[6:])
    print()
    print(r[0:3])
    print(r[3:6])
    print(r[6:])
    print()
    print(s[0:3])
    print(s[3:6])
    print(s[6:])

    if "y" in input("do you want to save? "):
        file = open("Files/saved_network", "w")
        net.write_to_file(file)
        file.close()
