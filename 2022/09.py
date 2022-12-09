import time
import re
from enum import Enum

import numpy as np

"""
  y
  
  ^
  |
  |
  +----> x
"""


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


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


MOVEMENT = {
    Direction.UP: Coords(0, 1),
    Direction.DOWN: Coords(0, -1),
    Direction.RIGHT: Coords(1, 0),
    Direction.LEFT: Coords(-1, 0),
}


def print_grid(head, tail):
    print('')
    for y in range(5, -1, -1):
        for x in range(0, 6, 1):
            if head.as_tuple() == (x, y):
                print('H', end='')
            elif tail.as_tuple() == (x, y):
                print('T', end='')
            elif (x, y) == (0, 0):
                print('s', end='')
            else:
                print('.', end='')
        print('')
    print('')


def get_input(test):
    filename = 'inputs/09_test2.txt' if test else 'inputs/09.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    commands = []
    for line in input_:
        dir = Direction(line[0])
        num = int(line[2:-1])
        commands.append((dir, num))

    return commands


def get_tail_dir(head, tail):
    # diagonal
    if (abs(head.x - tail.x) > 1 and abs(head.y - tail.y) > 0) or \
            (abs(head.x - tail.x) > 0 and abs(head.y - tail.y) > 1):
        return Coords(
            1 if head.x > tail.x else -1,
            1 if head.y > tail.y else -1,
        )
    # horizontal
    if abs(head.x - tail.x) > 1:
        return Coords(
            1 if head.x > tail.x else -1,
            0,
        )
    # vertical
    if abs(head.y - tail.y) > 1:
        return Coords(
            0,
            1 if head.y > tail.y else -1,
        )
    return Coords(0, 0)


def main(test):
    commands = get_input(test)
    head = Coords(0, 0)
    tail = Coords(0, 0)
    visited = set()

    for dir, num in commands:
        for _ in range(num):
            head += MOVEMENT[dir]
            tail += get_tail_dir(head, tail)
            visited.add(tail.as_tuple())

    print(len(visited))

    visited.clear()
    rope = [Coords(0, 0) for _ in range(10)]
    for dir, num in commands:
        for _ in range(num):
            rope[0].add(MOVEMENT[dir])
            for i in range(9):
                rope[i + 1].add(get_tail_dir(rope[i], rope[i + 1]))
                tail += get_tail_dir(head, tail)
            visited.add(rope[-1].as_tuple())
    print(len(visited))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
