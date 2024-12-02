#!/usr/bin/env python
import time


def get_input(test):
    left = []
    right = []
    filename = 'inputs/01_test.txt' if test else 'inputs/01.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data = line.split(' ')
            left.append(int(data[0]))
            right.append(int(data[-1]))
    return left, right


def main(test):
    left, right = get_input(test)
    left.sort()
    right.sort()
    sum1 = 0
    sum2 = 0
    for l, r in zip(left, right):
        sum1 += abs(l - r)
        sum2 += l * right.count(l)

    print('part1:', sum1)
    print('part2:', sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
