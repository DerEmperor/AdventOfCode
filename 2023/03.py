from __future__ import annotations

import time
from collections import defaultdict

CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def get_input(test):
    data = []
    filename = 'inputs/02_test.txt' if test else 'inputs/02.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test):
    data = get_input(test)
    for line in data:
        for i, c in enumerate(line):
            if c.isdigit():

                while is digit

                # search special char

                # add





if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
