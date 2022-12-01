from __future__ import annotations

import time
from typing import Tuple, List


def get_input(test: bool) -> List[str]:
    filename = 'inputs/01_test.txt' if test else 'inputs/01.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return input_


def main(test):
    input_ = get_input(test)

    calories_by_elv = [0]

    for line in input_:
        if line == '\n':
            calories_by_elv.append(0)
        else:
            num = int(line[:-1])
            calories_by_elv[-1] += num

    calories_by_elv.sort(reverse=True)
    print("part 1:", calories_by_elv[0])
    print("part 2:", sum(calories_by_elv[:3]))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')