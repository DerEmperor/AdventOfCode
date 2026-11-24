#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout

t_key = tuple[int, int, int, int, int]
t_lock = tuple[int, int, int, int, int]


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[list[str]]:
    data = [[]]
    filename = 'inputs/25_test.txt' if test else 'inputs/25.txt'
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                data.append([])
                continue
            data[-1].append(line[:-1])
    return data


def parse_input(data: list[list[str]]) -> tuple[list[t_key], list[t_lock]]:
    keys = []
    locks = []
    for entry in data:
        if entry[0][0] == '#':
            # lock
            lock = [0] * 5
            for line in entry[1:]:
                for i, c in enumerate(line):
                    if c == '#':
                        lock[i] += 1
            locks.append(tuple(lock))
        else:
            # key
            key = [0] * 5
            for line in entry[-2:0:-1]:
                for i, c in enumerate(line):
                    if c == '#':
                        key[i] += 1
            keys.append(tuple(key))

    return keys, locks


def solve(keys: list[t_key], locks: list[t_lock]) -> int:
    res = 0
    for key in keys:
        for lock in locks:
            if all([key[i] + lock[i] <= 5 for i in range(5)]):
                res += 1

    return res


def main(test: bool):
    data = get_input(test)
    keys, locks = parse_input(data)

    sum1 = solve(keys, locks)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [3, 3360]:
        raise WrongAnswer('part1')


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
