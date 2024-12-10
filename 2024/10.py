#!/usr/bin/env python
from __future__ import annotations

import time
from typing import List, Tuple


def get_input(test: bool):
    data = []
    filename = 'inputs/10_test.txt' if test else 'inputs/10.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append([int(x) for x in line[:-1]])
    return data


def get_score(data: List[List[int]], x: int, y: int) -> List[Tuple[int, int]]:
    if not (0 <= x < len(data[0]) and 0 <= y < len(data)):
        # oob
        return []
    if data[y][x] >= 9:
        return [(x, y)]

    res = []
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if 0 <= x + dx < len(data[0]) and 0 <= y + dy < len(data):
            if data[y + dy][x + dx] == data[y][x] + 1:
                res.extend(get_score(data, x + dx, y + dy))

    return res


def main(test: bool):
    data = get_input(test)
    part1 = 0
    part2 = 0

    for y, line in enumerate(data):
        for x, height in enumerate(line):
            if height == 0:
                res = get_score(data, x, y)
                part1 += len(set(res))
                part2 += len(res)

    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
