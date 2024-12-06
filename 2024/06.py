#!/usr/bin/env python
import time
from itertools import cycle

'''
+---> x
|
|
v
y
'''

directions = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])  # (x, y)


def get_input(test: bool):
    obstructions = set()
    start = None
    filename = 'inputs/06_test.txt' if test else 'inputs/06.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    dimensions = (len(input_[0]), len(input_))
    for y, line in enumerate(input_):
        for x, char in enumerate(line):
            if char == '#':
                obstructions.add((x, y))
            elif char == '^':
                assert start is None
                start = (x, y)
    assert start is not None
    return obstructions, start, dimensions


def main(test: bool):
    obstructions, start, dimensions = get_input(test)

    part2 = 0

    direction = next(directions)
    pos = start
    visited = set()

    while 0 <= pos[0] < dimensions[0] and 0 <= pos[1] < dimensions[1]:
        visited.add(pos)
        next_pos = pos[0] + direction[0], pos[1] + direction[1]
        if next_pos in obstructions:
            direction = next(directions)
        else:
            pos = next_pos

    print('part1:', len(visited))
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
