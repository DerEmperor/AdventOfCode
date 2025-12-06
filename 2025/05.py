#!/usr/bin/env python
import time
from typing import List, Tuple


def get_input(test: bool) -> Tuple[List[range], List[int]]:
    ranges = []
    numbers = []
    filename = 'inputs/05_test.txt' if test else 'inputs/05.txt'
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                break
            a, b = line[:-1].split('-')
            ranges.append(range(int(a), int(b)+1))

        for line in file:
            numbers.append(int(line[:-1]))
    return ranges, numbers


def main(test: bool):
    ranges, numbers = get_input(test)

    sum1 = 0
    sum2 = 0

    for n in numbers:
        for r in ranges:
            if n in r:
                sum1 += 1
                break

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