import time
import re
import numpy as np


def get_input(test):
    filename = 'inputs/08_test.txt' if test else 'inputs/08.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    trees = []
    for i, line in enumerate(input_):
        trees.append([])
        for c in line[:-1]:
            trees[i].append(int(c))
    return np.array(trees)


def main(test):
    trees = get_input(test)
    score = 0
    score2 = 0
    for y, line in enumerate(trees):
        for x, tree in enumerate(line):
            if (max(trees[y, :x], default=-1) < tree or max(trees[y, x + 1:], default=-1) < tree) or \
                    (max(trees[:y, x], default=-1) < tree or max(trees[y + 1:, x], default=-1) < tree):
                # tree is visible
                score += 1
            if x in (0, trees.shape[0] - 1) or y in (0, trees.shape[1] - 1):
                continue
            cur_score2 = 1
            for sight in (trees[y, x - 1::-1], trees[y, x + 1:], trees[y - 1::-1, x], trees[y + 1:, x]):
                tree_counter = 0
                for tree2 in sight:
                    tree_counter += 1
                    if tree2 >= tree:
                        break
                cur_score2 *= tree_counter

            score2 = max(score2, cur_score2)
    print(score)
    print(score2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
