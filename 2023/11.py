#!/usr/bin/env python
from __future__ import annotations

import time


def get_input(test: bool):
    data = []
    filename = 'inputs/11_test.txt' if test else 'inputs/11.txt'
    with open(filename, 'r') as file:
        input_ = file.read()
        data = [list(s) for s in input_.split('\n')[:-1]]

    return data


def print_grid(grid):
    for row in grid:
        for p in row:
            print(p, end='')
        print()
    print()


def expand_grid(grid):
    # rows
    for row in grid:
        if row.count('#') == 0:
            for y in range(len(row)):
                row[y] = '*'

    # columns
    x = 0
    while x < len(grid[0]):
        cnt = 0
        for y in range(len(grid)):
            if grid[y][x] == '#':
                cnt += 1
                break
        if cnt == 0:
            for row in grid:
                row[x] = '*'
            x += 2
        else:
            x += 1


def get_positions(grid):
    positions = []
    for y, row in enumerate(grid):
        for x, p in enumerate(row):
            if p == '#':
                positions.append((x, y))
    return positions


def main(test: bool):
    grid = get_input(test)
    expand_grid(grid)
    positions = get_positions(grid)

    factors = [
        2,
        10,
        100,
        1000000,
    ]

    for factor in factors:
        sum = 0
        for i, p1 in enumerate(positions):
            for p2 in positions[i + 1:]:

                for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])):
                    if grid[p1[1]][x] == '*':
                        sum += factor
                    else:
                        sum += 1

                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])):
                    if grid[y][p1[0]] == '*':
                        sum += factor
                    else:
                        sum += 1

        print(sum)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', round(executionTime, 2), 's')
    else:
        print('Execution time:', round(executionTime * 1000, 2), 'ms')
