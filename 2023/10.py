#!/usr/bin/env python
from __future__ import annotations

import time
from copy import deepcopy
from enum import Enum


class Dir(Enum):
    U = 'U'
    D = 'D'
    L = 'L'
    R = 'R'


U = Dir.U
D = Dir.D
L = Dir.L
R = Dir.R

PIPES = {'F': (D, R), '-': (L, R), '|': (D, U), '7': (D, L), 'L': (U, R), 'J': (L, U), }
MIRROR_DIR = {U: D, D: U, L: R, R: L}
STEPS = {U: (0, -1), D: (0, 1), L: (-1, 0), R: (1, 0)}


class IllegalPath(Exception):
    pass


def get_input(test: bool):
    data = []
    filename = 'inputs/10_test7.txt' if test else 'inputs/10.txt'
    with open(filename, 'r') as file:
        input_ = file.read()
        data = input_.split('\n')[:-1]

    return data


def find_start(data):
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == 'S':
                return x, y


def print_map(map):
    for line in map:
        for c in line:
            print(c, end='')
        print()
    print()


def get_maps(start, data):
    possible_dirs = []
    x, y = start

    # check left
    if x > 0 and data[y][x - 1] in 'F-L':
        possible_dirs.append(L)
    # check right
    if x < len(data) - 1 and data[y][x + 1] in '7-J':
        possible_dirs.append(R)
    # check up
    if y > 0 and data[y - 1][x] in 'F|7':
        possible_dirs.append(U)
    # check left
    if x < len(data[0]) - 1 and data[y + 1][x] in 'J|L':
        possible_dirs.append(D)

    # iterate through all pairs
    for i, d1 in enumerate(possible_dirs):
        for d2 in possible_dirs[i + 1:]:
            for k, v in PIPES.items():
                if v == (d1, d2) or v == (d2, d1):
                    data[y] = data[y][:x] + k + data[y][x + 1:]
                    yield data
                    break


def get_next_seperator(row, x):
    while x < len(row):
        if row[x] == '|':
            return x - 1, x + 1
        elif row[x] in 'FL':
            start = x + 1
            x += 1
            while row[x] == '-':
                x += 1
            if (row[start - 1] == 'F' and row[x] == 'J') or (row[start - 1] == 'L' and row[x] == '7'):
                return start, x + 1

            else:
                assert (row[start - 1] == 'F' and row[x] == '7') or (row[start - 1] == 'L' and row[x] == 'J')
                # look further
        x += 1
    return None


def main(test: bool):
    data = get_input(test)
    start = find_start(data)
    for map in get_maps(start, data):
        try:
            x, y = start
            steps = 0
            start_pipe = map[y][x]
            start_dir = PIPES[start_pipe][0]
            last_dir = MIRROR_DIR[start_dir]
            visited = [['.'] * len(row) for row in map]

            while True:
                # mark in visited
                visited[y][x] = map[y][x]

                # determine next dir
                incoming_dir = MIRROR_DIR[last_dir]
                possible_dirs = PIPES[map[y][x]]
                if incoming_dir == possible_dirs[0]:
                    next_dir = possible_dirs[1]
                elif incoming_dir == possible_dirs[1]:
                    next_dir = possible_dirs[0]
                else:
                    raise IllegalPath

                # take step
                dx, dy = STEPS[next_dir]
                x += dx
                y += dy
                steps += 1
                last_dir = next_dir

                if (x, y) == start:
                    break

        except IllegalPath:
            pass

        else:
            assert steps % 2 == 0
            print(steps // 2)

            # look vor visited
            #print_map(visited)
            inside_tiles = 0
            for y in range(len(visited)):
                x = 0
                while tmp := get_next_seperator(visited[y], x):
                    _, x = tmp
                    end, start = get_next_seperator(visited[y], x)
                    for i in range(x, end + 1):
                        if visited[y][i] == '.':
                            inside_tiles += 1
                            visited[y][i] = '#'
                    x = start
            #print_map(visited)
            print(inside_tiles)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
