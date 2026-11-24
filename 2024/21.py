#!/usr/bin/env python
import os
import sys
import time
from functools import cache

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[str]:
    data = []
    filename = 'inputs/21_test.txt' if test else 'inputs/21.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


# combine coords of both pads
COORDINATES = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
    '^': (1, 3),
    '<': (0, 4),
    'v': (1, 4),
    '>': (2, 4),
}


def get_paths(start: str, dst: str) -> list[str]:
    """all button sequences moving an arm from start to dst (and pressing it)"""
    (x1, y1), (x2, y2) = COORDINATES[start], COORDINATES[dst]
    dx = ('<' if x1 > x2 else '>') * abs(x1 - x2)
    dy = ('^' if y1 > y2 else 'v') * abs(y1 - y2)
    res = []
    for path in (dx + dy + 'A', dy + dx + 'A'):
        # the arm may never point at the gap in the top left corner
        x, y = x1, y1
        valid = True
        for c in path[:-1]:
            x += 1 if c == '>' else -1 if c == '<' else 0
            y += 1 if c == 'v' else -1 if c == '^' else 0
            if (x, y) == (0, 3):
                valid = False
                break
        if valid:
            res.append(path)
    return res


@cache
def get_moves(start: str, dst: str, depth: int, max_depth: int) -> int:
    if depth == max_depth:
        # human input
        return 1
    costs = []
    for path in get_paths(start, dst):
        path_res = 0
        pos = 'A'
        for c in path:
            path_res += get_moves(pos, c, depth + 1, max_depth)
            pos = c
        costs.append(path_res)
    return min(costs)


def solve(data: list[str], max_depth: int) -> int:
    res = 0
    for line in data:
        pos = 'A'
        presses = 0
        for c in line:
            presses += get_moves(pos, c, 0, max_depth)
            pos = c
        res += int(line[:-1]) * presses
    return res


def main(test: bool):
    data = get_input(test)

    # part 1: your keypad plus 2 robots; part 2: your keypad plus 25 robots
    sum1 = solve(data, 3)
    sum2 = solve(data, 26)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [126384, 156714]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [154115708116294, 191139369248202]:
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
