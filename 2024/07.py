#!/usr/bin/env python
import time
from statistics import multimode
from typing import List


def get_input(test: bool):
    data = []
    filename = 'inputs/07_test.txt' if test else 'inputs/07.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            line = line[:-1].replace(':', '')
            data.append([int(x) for x in line.split(' ')])
    return data


def get_number_possible_solutions(goal: int, numbers: List[int], concat:bool) -> bool:
    if len(numbers) == 0:
        return False
    if len(numbers) == 1:
        return goal == numbers[0]

    a = numbers.pop(0)
    b = numbers.pop(0)

    numbers.insert(0, a + b)
    if get_number_possible_solutions(goal, numbers, concat):
        return True
    numbers[0] = a * b
    if get_number_possible_solutions(goal, numbers, concat):
        return True
    if concat:
        numbers[0] = int(str(a) + str(b))
        if get_number_possible_solutions(goal, numbers, concat):
            return True

    numbers[0] = b
    numbers.insert(0, a)
    return False


def main(test: bool):
    data = get_input(test)
    part1 = 0
    part2 = 0

    for line in data:
        if get_number_possible_solutions(line[0], line[1:], False):
            part1 += line[0]
            part2 += line[0]
        elif get_number_possible_solutions(line[0], line[1:], True):
            part2 += line[0]

    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
