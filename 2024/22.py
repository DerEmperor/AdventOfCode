#!/usr/bin/env python
import os
import sys
import time
from collections import defaultdict
from functools import cache

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[int]:
    data = []
    filename = 'inputs/22_test.txt' if test else 'inputs/22.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(int(line[:-1]))
    return data


def next_secret(num: int) -> int:
    num ^= num * 64
    num %= 16777216
    num ^= num // 32
    num %= 16777216
    num ^= num * 2048
    num %= 16777216
    return num


def part1(data: list[int]) -> tuple[int, list[list[tuple[int, int]]]]:
    res = 0
    numbers = []
    for num in data:
        numbers.append([])
        numbers[-1].append((num % 10, None))
        for _ in range(2000):
            next_num = next_secret(num)
            change = next_num % 10 - num % 10
            numbers[-1].append((next_num % 10, change))
            num = next_num
        res += num
    return res, numbers


def get_bananas_per_seq(nums: list[tuple[int, int]]) -> dict[tuple[int, int, int, int], int]:
    res = {}
    for i in range(4, len(nums)):
        a, b, c, d = nums[i - 3][1], nums[i - 2][1], nums[i - 1][1], nums[i][1]
        if (a, b, c, d) not in res:
            res[(a, b, c, d)] = nums[i][0]
    return res


def part2(numbers: list[list[tuple[int, int]]]) -> int:
    # calc bananas per sequence
    res = defaultdict(int)
    for nums in numbers:
        bananas_per_seq = get_bananas_per_seq(nums)
        for seq, bananas in bananas_per_seq.items():
            res[seq] += bananas
    return max(res.values())


def main(test: bool):
    data = get_input(test)

    sum1, numbers = part1(data)
    sum2 = part2(numbers)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [37327623, 18261820068, ]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [23, 24, 2044]:
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
