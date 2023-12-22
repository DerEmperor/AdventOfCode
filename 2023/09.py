#!/usr/bin/env python
from __future__ import annotations

import re
import time
from copy import deepcopy
from functools import cached_property
from itertools import groupby, cycle
from math import lcm
from typing import List


def get_input(test: bool):
    data = []
    filename = 'inputs/09_test.txt' if test else 'inputs/09.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        input_ = ['5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25\n']
        for line in input_:
            data.append([int(x) for x in line[:-1].split()])
    return data


def print_pyramid(pyramid):
    # Loop through each row
    for i, row in enumerate(pyramid):
        print('  ' * i, end='')

        for num in row:
            print('{:3s}'.format(str(num)), end=' ')
        print()
    print()


def main(test: bool):
    data = get_input(test)
    sum1 = 0
    sum2 = 0
    for line in data:
        pyramid = [line]
        # go down
        while any(x != 0 for x in pyramid[-1]):
            pyramid.append([(b - a) for a, b in zip(pyramid[-1][:-1], pyramid[-1][1:])])
        pyramid_cpy = deepcopy(pyramid)
        # part1
        # go up
        pyramid[-1].append(0)
        for i in range(len(pyramid) - 1, 0, -1):
            pyramid[i - 1].append(pyramid[i - 1][-1] + pyramid[i][-1])
        sum1 += pyramid[0][-1]

        # part 2
        pyramid = pyramid_cpy
        for i in range(len(pyramid) - 2, -1, -1):
            pyramid[i].insert(0, ' ')  # for printing
        pyramid[-1].insert(0, 0)
        for i in range(len(pyramid) - 1, 0, -1):
            pyramid[i - 1][0] = pyramid[i - 1][1] - pyramid[i][0]
        sum2 += pyramid[0][0]
    print(sum1, sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
