from simple_neural_network import *
from Evolutionary_NN.Population import Population
import random


def decrypt_file(file):
    solution_translator = {0: [1, 0, 0, 0], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0], 3: [0, 0, 0, 1]}
    situations = []
    solutions = []
    for line in file:
        line = line.strip()
        info = line.split(',')
        solution = solution_translator[int(info[-1])]
        situation = [int(i) for i in info[:len(info)-1]]
        solutions.append(solution)
        situations.append(situation)
    return situations, solutions


def write_board(file, board, direction):
    for row in board:
        for spot in row:
            file.write(str(spot) + ",")
    direction_vals = {"left": 0, "up": 1, "right": 2, "down": 3}
    file.write(str(direction_vals[direction]))
    file.write("\n")


def extreme(the_list):
    top = max(the_list)
    top_index = the_list.index(top)
    new_list = [0 for i in range(len(the_list))]
    new_list[top_index] = 1
    return new_list


def convert_output_to_action(output):
    if output == [1, 0, 0, 0]:
        return "left"
    if output == [0, 1, 0, 0]:
        return "up"
    if output == [0, 0, 1, 0]:
        return "right"
    if output == [0, 0, 0, 1]:
        return "down"

# created jan 2, 2020
w = 20
l = 20
head_val = 2
body_val = 1
apple_val = 3
apple_score = 1000
survive_score = 5
hit_wall = -1000
hit_body = -1000
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


def draw_board(b):
    window.fill(BLACK)
    # print_board(b)
    for r, row in enumerate(b):
        for c, spot in enumerate(row):
            color = GREEN
            if spot == 0:
                color = BLACK
            if spot == apple_val:
                color = RED
            pygame.draw.rect(window, color, [c*box_width, r*box_height, box_width, box_height])


class Snake:
    def __init__(self, board):
        r, c = index_2d(board, head_val)
        self.head = (r, c)
        self.body = []
        self.just_ate = False
        self.eat_apple()
        self.eat_apple()

    def move(self, action):
        for i, body_seg in enumerate(reversed(self.body), start=1):
            if i == 1 and self.just_ate:
                continue
            if i < len(self.body) - 1:
                self.body[-i] = self.body[-(i+1)]
            else:
                self.body[-i] = self.head
        r, c = self.head
        if action == "up":
            r -= 1
        elif action == "down":
            r += 1
        elif action == "right":
            c += 1
        elif action == "left":
            c -= 1
        self.head = (r, c)
        self.just_ate = False

    def eat_apple(self):
        self.just_ate = True
        if len(self.body) > 0:
            self.body.append(self.body[-1])
        else:
            self.body.append(self.head)


def index_2d(board, val):
    for r, row in enumerate(board):
        if val in row:
            return r, row.index(val)
    return None


def make_apple(b):
    x, y = random.randint(0, w - 1), random.randint(0, l - 1)
    while b[x][y] != 0:
        x, y = random.randint(0, w - 1), random.randint(0, l - 1)
    b[x][y] = apple_val
    return b


def create_board():
    new_board = [[0 for i in range(w)] for j in range(l)]
    new_board[l//2][w//2] = head_val
    snek = Snake(new_board)
    make_apple(new_board)
    return new_board, snek


def score_board(board, action):
    if board is None:
        return -10000
    r, c = index_2d(board, head_val)
    try:
        if action == "up":
            r -= 1
        elif action == "down":
            r += 1
        elif action == "right":
            c += 1
        elif action == "left":
            c -= 1
        if r < 0 or c < 0:
            return hit_wall
        if board[r][c] == body_val:
            return hit_body
    except IndexError:
        return hit_wall
    apple = index_2d(board, apple_val)
    if apple == (r, c):
        return apple_score
    return survive_score


def update_board(b, action, snek):
    score = score_board(b, action)
    if score == hit_wall or score == hit_body:  # if hit a wall
        return None
    if score == apple_score:  # if ate
        snek.eat_apple()
        b = make_apple(b)
    elif len(snek.body) > 0:
        r, c = snek.body[-1]  # get the back of the body
        b[r][c] = 0
    else:
        r, c = snek.head
        b[r][c] = 0
    snek.move(action)
    if len(snek.body) > 0:
        r2, c2 = snek.body[0]
        b[r2][c2] = body_val
    r1, c1 = snek.head
    b[r1][c1] = head_val
    return b


def print_board(board):
    for row in board:
        print(row)
    print()


def manual():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        return "left"
    if keys[pygame.K_RIGHT]:
        return "right"
    if keys[pygame.K_UP]:
        return "up"
    if keys[pygame.K_DOWN]:
        return "down"
    try:
        return action
    except NameError:
        return "right"


def play_net(net):
    board, snek = create_board()
    played_situations = []
    run = True
    while run:
        pygame.time.delay(delay)
        if drawing and board is not None:
            draw_board(board)
            pygame.display.update()
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    run = False
        if not run or board is None:
            break
        action = convert_output_to_action(extreme(net.get_chances(cast_rays(board))))
        reward = score_board(board, action)
        if reward == apple_score:
            print("refresh")
            played_situations = []
        elif (snek.head, snek.body) in played_situations:
            print("loop")
            break
        else:
            played_situations.append((snek.head, snek.body))
        board = update_board(board, action, snek)


def test_net(net):
    score = 0
    played_situations = []
    max_ticks = 50
    board, snek = create_board()
    while True:
        chances = net.get_chances(cast_rays(board))
        # print(chances)
        action = convert_output_to_action(extreme(chances))
        # print(action)
        reward = score_board(board, action)
        score += reward
        #ticks_since_score = ticks_since_score + 1 if reward != apple_score else 0
        if reward == apple_score:
            # print("refresh")
            played_situations = []
        elif (snek.head, snek.body) in played_situations:
            return score + survive_score * 10 # (max_ticks - len(played_situations))
        else:
            played_situations.append((snek.head, snek.body))
        board = update_board(board, action, snek)
        if board is None:
            return score


def test_generation(population):
    scores = []
    trials = 10
    for net in population.population:
        score = 0
        for i in range(trials):
            val = test_net(net)
            score += val
        scores.append(score)

    return scores


def cast_rays(b):
    r1, c1 = index_2d(b, head_val)
    r2, c2 = index_2d(b, apple_val)
    x_to_apple = c1 - c2
    y_to_apple = r1 - r2
    up_cast_wall = r1
    up_cast_apple = up_cast_wall if c1 != c2 or r2 < r1 else r2 - r1
    down_cast_wall = len(b) - r1
    down_cast_apple = down_cast_wall if c1 != c2 or r2 > r1 else r1 - r2
    left_cast_wall = c1
    left_cast_apple = left_cast_wall if r1 != r2 or c2 < c1 else c2 - c1
    right_cast_wall = len(b[0]) - c1
    right_cast_apple = right_cast_wall if r1 != r2 or c2 > c1 else c1 - c2
    for r in range(0, r1):
        if b[r][c1] == body_val:
            up_cast_wall = r1 - r
    for r in range(r1, len(b)):
        if board[r][c1] == body_val:
            down_cast_wall = r-r1
            break
    for c in range(0, c1):
        if b[r1][c] == body_val:
            left_cast_wall = c1 - c
    for c in range(c1, len(b[0])):
        if board[r1][c] == body_val:
            right_cast_wall = c-c1
            break
    #'''
    rays = [up_cast_wall, up_cast_apple,
            right_cast_wall, right_cast_apple,
            down_cast_wall, down_cast_apple,
            left_cast_wall, left_cast_apple]
    #'''
    #rays = [up_cast_wall, right_cast_wall, down_cast_wall, left_cast_wall, x_to_apple, y_to_apple]
    # print((r1, c1), rays)
    return rays


if __name__ == '__main__':
    player = False
    drawing = True
    delay = 0
    board, snek = create_board()
    if drawing:
        import pygame
        pygame.init()
        window_width = 500
        window_height = 500
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("snake game")
        ScreenColor = BLACK
        box_width = window_width // w
        box_height = window_height // l
        print(box_width, box_height)
    if not player:
        amount_of_generations = 1500
        size_of_population = 500
        layers = (6, 12, 10, 4)
        activation = [NeuralNetwork.leaky_relu, NeuralNetwork.leaky_relu, NeuralNetwork.leaky_relu]
        net = NeuralNetwork(layers, activation)
        net.insert_weights_from_file(open("Files/saved_network", 'r'))
        while True:
            play_net(net)
        pop = Population(size_of_population, layers, activation, mutation_rate=.1, survival_rate=.1)
        pop.population.append(net)
        for i in range(amount_of_generations):
            print("generation test", i)
            test = test_generation(pop)
            pop.play_generation(test, high_bad=False)
            print(sorted(test))
            # print(pop.population[0])
            print(sorted(test)[-1])
            if i > 100:
                play_net(pop.population[0])
                pop.population[0].write_to_file(open("Files/saved_network", 'w'))
        pop.sort_population(test_generation(pop))
        net = pop.population[0]
        net.write_to_file(open('Files/saved_network', 'w'))
        '''
        with open("Files/snake_data", 'r') as file:
            data, answers = decrypt_file(file)
            test, test_answer = data.pop(), answers.pop()
            print(len(data))
        layers = (400, 50, 4)
        activation = (NeuralNetwork.tanh, NeuralNetwork.tanh)
        net = NeuralNetwork(layers, activation)
        net.train_network(data, answers, .1, 10)
        '''
    run = True
    if player:
        write_file = open('Files/snake_data', 'w')
    while run:
        pygame.time.delay(delay)
        if drawing and board is not None:
            draw_board(board)
            pygame.display.update()
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    run = False
        if not run or board is None:
            break
        action = manual() if player else convert_output_to_action(extreme(net.get_chances(flatten(board))))
        board = update_board(board, action, snek)
        if player:
            write_board(write_file, board, action)
    write_file.close()


