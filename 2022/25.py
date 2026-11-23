#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[str]:
    data = []
    filename = 'inputs/25_test.txt' if test else 'inputs/25.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


DECODE = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}


def snafu2dec(val: str) -> int:
    factor = 1
    res = 0
    for c in val[::-1]:
        res += factor * DECODE[c]
        factor *= 5
    return res


def dec2snafu(val: int) -> str:
    if val == 0:
        return '0'

    digits = "012=-0"
    result = ""
    overflow = False
    while val > 0:
        digit = val % 5 + int(overflow)
        overflow = digit >= 3
        digit = digits[digit]
        result = digit + result
        val //= 5
    if overflow:
        result = '1' + result

    return result


def part1(data: list[str]) -> str:
    res = 0
    for val in data:
        res += snafu2dec(val)
    return dec2snafu(res)


def main(test: bool):
    data = get_input(test)

    sum1 = part1(data)
    sum2 = 0

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in ['2=-1=0', '2-==10--=-0101==1201']:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [0, ]:
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
