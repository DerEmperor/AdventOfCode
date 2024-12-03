#!/usr/bin/env python
import time


def get_input(test):
    data = []
    filename = 'inputs/04_test.txt' if test else 'inputs/04.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test):
    data = get_input(test)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')