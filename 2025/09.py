#!/usr/bin/env python
import os
import sys
import time
from collections import defaultdict
from typing import List, Tuple, Dict

original_stdout = sys.stdout

Coordinates = Tuple[int, int]


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> List[Coordinates]:
    data = []
    filename = 'inputs/09_test.txt' if test else 'inputs/09.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(tuple(int(n) for n in line[:-1].split(',')))
    return data


def main(test: bool):
    red_tiles = get_input(test)

    sum1 = 0
    sum2 = 0

    # part 1
    for i, c1 in enumerate(red_tiles):
        x1, y1 = c1
        for c2 in red_tiles[i + 1:]:
            x2, y2 = c2
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > sum1:
                sum1 = area

    # part2
    # get border
    # store tiles as ranges, key: y-coordinate, values: x-coordinates of tiles
    # This is not a general solution, but works for this problem
    borders_from_y: Dict[int, List[int]] = defaultdict(list)
    for i, c1 in enumerate(red_tiles):
        c2 = red_tiles[i - 1]
        x1, y1 = c1
        x2, y2 = c2
        if x1 == x2:
           for y in range(min(y1, y2), max(y1, y2) + 1):
               borders_from_y[y].append(x1)
        elif y1 == y2:
            borders_from_y[y1].extend([x1, x2])
        else:
            raise Exception('coordinates are not in a line')

    tiles_from_y: Dict[int, range] = {}
    for y, vals in borders_from_y.items():
        tiles_from_y[y] = range(min(vals), max(vals) + 1)

    sys.stdout = original_stdout  # enable print
    for i, c1 in enumerate(red_tiles):
        print(f'\r{i}/{len(red_tiles)}', end='')
        x1, y1 = c1
        for c2 in red_tiles[i + 1:]:
            x2, y2 = c2
            # check if everywhere are tiles
            all_tiles = True
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if x1 not in tiles_from_y[y] or x2 not in tiles_from_y[y]:
                    all_tiles = False
                    break

            if all_tiles:
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                if area > sum2:
                    sum2 = area
    print('\r                    \r', end='')

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [50, 4748769124]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [24, 1525991432]:
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
