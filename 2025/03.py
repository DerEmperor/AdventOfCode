#!/usr/bin/env python
import time
from typing import List


def get_input(test: bool) -> List[List[int]]:
    data = []
    filename = 'inputs/03_test.txt' if test else 'inputs/03.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append([int(n) for n in line[:-1]])
    return data


def get_max_joltage(bank: List[int]) -> int:
    # first digit
    cur_max_idx = 0
    cur_max_val = bank[0]
    for i, n in enumerate(bank[1:-1], start=1):
        if n > cur_max_val:
            cur_max_val = n
            cur_max_idx = i

    res = cur_max_val * 10

    # second digit
    cur_max_val = bank[cur_max_idx + 1]
    for n in bank[cur_max_idx + 2:]:
        if n > cur_max_val:
            cur_max_val = n

    res += cur_max_val

    return res


def get_max_joltage2(bank: List[int]) -> int:
    res = 0

    cur_max_idx = -1
    for i in range(11, -1, -1):
        cur_max_val = bank[cur_max_idx + 1]
        cur_max_idx = cur_max_idx + 1
        for j, n in enumerate(bank[cur_max_idx + 1:-i] if i != 0 else bank[cur_max_idx + 1:], start=cur_max_idx + 1):
            if n > cur_max_val:
                cur_max_val = n
                cur_max_idx = j

        res += cur_max_val * (10 ** i)

    return res


def main(test: bool):
    data = get_input(test)

    sum1 = 0
    sum2 = 0

    for bank in data:
        res = get_max_joltage(bank)
        sum1 += res
        res = get_max_joltage2(bank)
        sum2 += res

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
