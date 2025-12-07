#!/usr/bin/env python
import math
import time
from typing import List


def get_input(test: bool) -> List[str]:
    data = []
    filename = 'inputs/06_test.txt' if test else 'inputs/06.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def fix_data(data: List[str]) -> List[str]:
    """pycharm removes trailing spaces, so we need to fix it"""
    length = max(len(row) for row in data)
    for i, row in enumerate(data):
        if len(row) < length:
            row += ' ' * (length - len(row))
            data[i] = row

    return data


def calculate(op: str, nums_str: List[str], transpose: bool) -> int:
    if transpose:
        nums_str = [''.join(col) for col in zip(*nums_str)]
    nums = [int(n.strip()) for n in nums_str]
    if '*' in op:
        return math.prod(nums)
    elif '+' in op:
        return sum(nums)
    else:
        raise Exception('invalid operation:' + op)


def main(test: bool):
    data = get_input(test)
    data = fix_data(data)

    sum1 = 0
    sum2 = 0

    res = 0
    op = ''
    nums_str = ['' for _ in range(len(data) - 1)]
    for j in range(len(data[0])):
        if all(data[i][j] == ' ' for i in range(len(data))):

            sum1 += calculate(op, nums_str, False)
            sum2 += calculate(op, nums_str, True)

            # reset data
            op = ''
            nums_str = ['' for _ in range(len(data) - 1)]
        else:
            op += data[-1][j]
            for i in range(len(data) - 1):
                nums_str[i] += data[i][j]

    sum1 += calculate(op, nums_str, False)
    sum2 += calculate(op, nums_str, True)

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
