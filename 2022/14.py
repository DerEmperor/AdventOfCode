from __future__ import annotations
import time
import re
from functools import cmp_to_key
from enum import Enum
import numpy as np


class Point(Enum):
    air = '.'
    sand = 'o'
    rock = '#'


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def as_tuple(self):
        return self.x, self.y


DOWN = Coords(0, 1)
LEFT = Coords(-1, 1)
RIGHT = Coords(1, 1)
part1 = True

def get_input(test):
    filename = 'inputs/14_test.txt' if test else 'inputs/14.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    data = []
    for line in input_:
        data.append([])
        for coords in line[:-1].split(' -> '):
            x, y = coords.split(',')
            data[-1].append(Coords(int(x), int(y)))

    return data


def main(test):
    data = get_input(test)
    size = (500, 0)
    for line in data:
        size = (max(size[0], *[c.x + 1 for c in line]), max(size[1], *[c.y for c in line]))

    size = (size[0] + 100, size[1] + 3)
    grid = []
    for y in range(size[1] - 1):
        grid.append([])
        for x in range(size[0]):
            grid[-1].append(Point.air)

    grid.append([])
    for x in range(size[0]):
        grid[-1].append(Point.air if part1 else Point.rock)

    for line in data:
        for i in range(len(line) - 1):
            start, end = line[i], line[i + 1]
            if start.x == end.x:
                x = start.x
                for y in range(start.y, end.y + 1 if start.y < end.y else end.y - 1, 1 if start.y < end.y else -1):
                    grid[y][x] = Point.rock
            else:
                assert start.y == end.y
                y = start.y
                for x in range(start.x, end.x + 1 if start.x < end.x else end.x - 1, 1 if start.x < end.x else -1):
                    grid[y][x] = Point.rock

    score = 0
    end = False
    while not end:
        if grid[0][500] == Point.sand:
            score += 1
            break
        sand = Coords(500, 0)
        while True:
            if part1 and sand.y + 1 >= size[1]:
                end = True
                break

            if grid[sand.y + 1][sand.x] == Point.air:
                sand.add(DOWN)
                continue

            if grid[sand.y + 1][sand.x - 1] == Point.air:
                sand.add(LEFT)
                continue

            if grid[sand.y + 1][sand.x + 1] == Point.air:
                sand.add(RIGHT)
                continue
            break
        grid[sand.y][sand.x] = Point.sand
        score += 1

    print(score-1)


if __name__ == '__main__':
    startTime = time.time()

    print('part 1')
    print('Test')
    main(True)
    print('real')
    main(False)
    part1 = False
    print()
    print('part 2')
    print('Test')
    main(True)
    print('real')
    main(False)


    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
