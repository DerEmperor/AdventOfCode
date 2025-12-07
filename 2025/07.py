#!/usr/bin/env python
import time
from collections import defaultdict
from typing import List


def get_input(test: bool) -> List[str]:
    data = []
    filename = 'inputs/07_test.txt' if test else 'inputs/07.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test: bool):
    data = get_input(test)

    sum1 = 0
    sum2 = 1
    indices = defaultdict(int)
    indices[data[0].find('S')] = 1
    for line in data[1:]:
        new_indices = defaultdict(int)
        for index, cnt in indices.items():
            if line[index] == '.':
                new_indices[index] += cnt
            elif line[index] == '^':
                sum1 += 1
                sum2 += cnt
                new_indices[index - 1] += cnt
                new_indices[index + 1] += cnt
            else:
                raise Exception('Invalid character' + line[index])
        indices = new_indices

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
