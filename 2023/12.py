#!/usr/bin/env python
"""
runtime:
test
part 1: 1,8s
part 2:
real:
part 1:
part 2:
"""
from __future__ import annotations

import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List, Tuple


def get_input(test: bool):
    data = []
    filename = f"inputs/{Path(__file__).stem}{'_test' if test else ''}.txt"
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            springs, checksum = line[:-1].split(' ')
            checksum = [int(x) for x in checksum.split(',')]
            data.append((list(springs), checksum))
    return data


def get_checksum(springs: List[str]) -> List[int]:
    res = []
    i = 0
    while i < len(springs):
        assert springs[i] != '?'
        if springs[i] == '#':
            cnt = 1
            i += 1
            while i < len(springs) and springs[i] == '#':
                cnt += 1
                i += 1
            res.append(cnt)
        i += 1
    return res


def helper(springs: List[str], checksum: List[int], i: int) -> int:
    while i < len(springs) and springs[i] != '?':
        i += 1

    if i == len(springs):
        if checksum == get_checksum(springs):
            return 1
        else:
            return 0

    springs[i] = '#'
    a = helper(springs, checksum, i + 1)
    springs[i] = '.'
    b = helper(springs, checksum, i + 1)
    springs[i] = '?'
    return a + b


def helper_caller(args: Tuple[List[str], List[int]]) -> int:
    springs, checksum = args
    return helper(springs, checksum, 0)


def helper_caller2(args: Tuple[List[str], List[int]]) -> int:
    springs, checksum = args
    springs = springs * 5
    checksum = checksum * 5
    return helper(springs, checksum, 0)


def main(test: bool):
    data = get_input(test)
    sum1 = 0
    with ProcessPoolExecutor() as executor:
        for possible_arrangements in executor.map(helper_caller, data):
            sum1 += possible_arrangements
    print(sum1)
    sys.stdout.flush()

    sum2 = 0
    with ProcessPoolExecutor() as executor:
        for possible_arrangements in executor.map(helper_caller2, data):
            sum2 += possible_arrangements
    print(sum2)
    sys.stdout.flush()


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    #main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', round(executionTime, 2), 's')
    else:
        print('Execution time:', round(executionTime * 1000, 2), 'ms')
