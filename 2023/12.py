#!/usr/bin/env python
"""
Execution time:
sum: 5,5 min
"""
from __future__ import annotations

import functools
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List, Tuple

def get_input(test: bool) -> List[Tuple[str, Tuple[int, ...]]]:
    data = []
    filename = f"inputs/{Path(__file__).stem}{'_test' if test else ''}.txt"
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            springs, checksum = line[:-1].split(' ')
            checksum = tuple(int(x) for x in checksum.split(','))
            new_springs = springs.replace('..', '.')
            while new_springs != springs:
                springs = new_springs
                new_springs = springs.replace('..', '.')
            data.append((springs, checksum))
    return data


mem = {}


def get_checksum(springs: str) -> Tuple[int, ...]:
    if len(springs) < 30:
        res = mem.get(springs, None)
        if res is not None:
            return res

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
    res = tuple(res)
    if len(springs) < 30:
        mem[springs] = res
    return res


def str_repl(string: str, i: int, c: str):
    return string[:i] + c + string[i + 1:]


def helper(springs: str, checksum: Tuple[int, ...], i: int) -> int:
    while i < len(springs) and springs[i] != '?':
        i += 1

    if i == len(springs):
        if checksum == get_checksum(springs):
            return 1
        else:
            return 0

    part_checksum = get_checksum(springs[:i])
    if len(part_checksum) > len(checksum):
        return 0
    if len(part_checksum) > 1 and part_checksum[:-1] != checksum[:len(part_checksum) - 1]:
        return 0
    if len(part_checksum) > 0 and part_checksum[-1] > checksum[len(part_checksum) - 1]:
        return 0

    new_springs = str_repl(springs, i, '#')
    a = helper(new_springs, checksum, i + 1)
    new_springs = str_repl(springs, i, '.')
    b = helper(new_springs, checksum, i + 1)
    return a + b


def helper_caller(args: Tuple[str, Tuple[int, ...]]) -> int:
    springs, checksum = args
    return helper(springs, checksum, 0)


def helper_caller2(args: Tuple[str, Tuple[int, ...]]) -> int:
    springs, checksum = args
    springs = ((springs + '?') * 5)[:-1]
    checksum = checksum * 5
    return helper(springs, checksum, 0)


def main(test: bool):
    data = get_input(test)
    single_thread = False
    for part, fun in [(1, helper_caller), (2, helper_caller2)]:
        # single thread
        sum = 0
        if single_thread:
            for i, chunk in enumerate(data):
                res = helper_caller2(chunk)
                print('\rprogress:', i, '/', len(data), end='', flush=True)
                sum += res
        else:
            i = 0
            with ProcessPoolExecutor() as executor:
                for possible_arrangements in executor.map(fun, data):
                    sum += possible_arrangements
                    i += 1
                    print('\rprogress:', i, '/', len(data), end='', flush=True)
                    sys.stdout.flush()
        print('\rpart ', part, ':', sum)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', round(executionTime, 2), 's')
    else:
        print('Execution time:', round(executionTime * 1000, 2), 'ms')
