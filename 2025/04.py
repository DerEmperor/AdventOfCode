#!/usr/bin/env python
import time
from operator import truediv
from typing import Tuple, Set


def get_input(test: bool) -> Set[Tuple[int, int]]:
    data = set()
    filename = 'inputs/04_test.txt' if test else 'inputs/04.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for y, line in enumerate(input_):
            for x, char in enumerate(line[:-1]):
                if char == '@':
                    data.add((x, y))
    return data


directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]


def main(test: bool):
    data = get_input(test)

    sum1 = 0
    sum2 = 0

    # part 1
    for x, y in data:
        cnt = 0
        for dx, dy in directions:
            if (x + dx, y + dy) in data:
                cnt += 1
        if cnt < 4:
            sum1 += 1

    # part2
    todo = True
    while todo:
        todo = False
        for x, y in data.copy():
            cnt = 0
            for dx, dy in directions:
                if (x + dx, y + dy) in data:
                    cnt += 1
            if cnt < 4:
                sum2 += 1
                todo = True
                data.remove((x, y))


    print('part1:', sum1)
    print('part2:', sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)

    if executionTime < 60:
        print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
    else:
        print(f'Execution time: {round(executionTime, 3)} s')
