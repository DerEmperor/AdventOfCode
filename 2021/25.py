#!/usr/bin/env python
import os
import sys
import time
from copy import deepcopy

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[list[str]]:
    data = []
    filename = 'inputs/25_test.txt' if test else 'inputs/25.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(list(line[:-1]))
    return data


def part1(field: list[list[str]]):
    moved = True
    steps = 0
    n = len(field[0])
    m = len(field)
    while moved:
        moved = False
        print('\r', steps, end='')
        steps += 1
        # east
        for y in range(m):
            last_can_move = field[y][-1] == '>' and field[y][0] == '.'
            x=0
            while x < n-1:
                if field[y][x] == '>' and field[y][(x + 1) % n] == '.':
                    moved = True
                    field[y][x] = '.'
                    field[y][(x + 1) % n] = '>'
                    x += 1
                x += 1
            if last_can_move:
                moved = True
                field[y][-1] = '.'
                field[y][0] = '>'
        # south
        for x in range(n):
            last_can_move = field[-1][x] == 'v' and field[0][x] == '.'
            y=0
            while y < m-1:
                if field[y][x] == 'v' and field[(y + 1) % m][x] == '.':
                    moved = True
                    field[y][x] = '.'
                    field[(y + 1) % m][x] = 'v'
                    y += 1
                y += 1
            if last_can_move:
                moved = True
                field[-1][x] = '.'
                field[0][x] = 'v'
    print('\r             \r', end='')
    return steps


def main(test: bool):
    data = get_input(test)

    sum1 = part1(deepcopy(data))
    sum2 = 0

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [58, 374]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [0, ]:
        raise WrongAnswer('part2')


if __name__ == '__main__':
    startTime = time.time()

    try:
        print('Test')
        main(True)
        print('real')
        sys.stdout = open(os.devnull, 'w')  # suppress test prints
        main(False)

    finally:
        executionTime = (time.time() - startTime)

        if executionTime < 60:
            print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
        else:
            print(f'Execution time: {round(executionTime, 3)} s')
