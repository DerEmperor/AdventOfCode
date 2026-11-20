#!/usr/bin/env python
import json
import os
import sys
import time
from unittest import case

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


class IllegalDivision(Exception):
    pass


def get_input(test: bool) -> dict[str, str | int | None]:
    data = {}
    filename = 'inputs/21_test.txt' if test else 'inputs/21.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            k, v = line.strip().split(': ')
            if v.isdigit():
                v = int(v)
            data[k] = v
    return data


def part1(monkeys: dict[str, str | int | None], monkey: str):
    val = monkeys[monkey]
    if val is None:
        return None
    elif isinstance(val, int):
        return val
    a, op, b = val.split()
    a = part1(monkeys, a)
    b = part1(monkeys, b)
    if a is None or b is None:
        return None
    else:
        match op:
            case '+':
                res = a + b
            case '-':
                res = a - b
            case '*':
                res = a * b
            case '/':
                if a % b != 0:
                    raise IllegalDivision()
                res = a // b
            case _:
                assert False, 'illegal operator'
    if monkey != 'root':
        monkeys[monkey] = res
    return res


def part2(monkeys: dict[str, str | int | None]) -> int:
    # get all monkeys that are possible
    monkeys['humn'] = None
    part1(monkeys, 'root')
    a, op, b = monkeys['root'].split()
    if isinstance(monkeys[a], int):
        goal = monkeys[a]
        next = b
    else:
        assert isinstance(monkeys[b], int)
        goal = monkeys[b]
        next = a
    while next != 'humn':
        a, op, b = monkeys[next].split()

        if isinstance(monkeys[a], int):
            x = monkeys[a]
            next = b
            known_left = True
        else:
            assert isinstance(monkeys[b], int)
            x = monkeys[b]
            next = a
            known_left = False
        match op:
            case '+':
                goal -= x
            case '-':
                if known_left:
                    goal = x - goal
                else:
                    goal += x
            case '*':
                goal //= x
            case '/':
                if known_left:
                    goal = x // goal
                else:
                    goal *= x

    return goal


def main(test: bool):
    monkeys = get_input(test)

    sum1 = part1(monkeys.copy(), 'root')
    sum2 = part2(monkeys)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [152, 282285213953670]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [301, 3699945358564]:
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
