#!/usr/bin/env python
import os
import sys
import time
from typing import List, Tuple

original_stdout = sys.stdout
Present_Raw = Tuple[str]
Dimension = Tuple[int, int]
Problem = Tuple[Dimension, List[int]]


class WrongAnswer(Exception):
    pass


class Presents:
    def __init__(self, presents: List[Present_Raw]):
        self.presents = presents
        self.presents_size = []
        for present in presents:
            size = sum(line.count('#') for line in present)
            self.presents_size.append(size)

    def problem_solvable(self, problem: Problem) -> bool:
        # do presents fit as blocks?
        dimensions, indices = problem
        if sum(indices) <= dimensions[0]//3 * dimensions[1]//3:
            return True

        # do presents fit at all
        space_needed = sum(i * s for i, s in zip(indices, self.presents_size))
        if space_needed > dimensions[0] * dimensions[1]:
            return False

        # pack items
        # Turns out, the complicated part is not needed

        return False


def get_input(test: bool) -> Tuple[List[Present_Raw], List[Problem]]:
    presents = []
    problems = []
    filename = 'inputs/12_test.txt' if test else 'inputs/12.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        parts = [[]]
        for line in input_:
            if line == '\n':
                parts.append([])
            else:
                parts[-1].append(line[:-1])

        for part in parts[:-1]:
            presents.append([])
            for line in part[1:]:
                presents[-1].append(line)
            presents[-1] = tuple(presents[-1])

        for line in parts[-1]:
            dimensions, indices = line.split(': ')
            dimensions = tuple(int(n) for n in dimensions.split('x'))
            indices = tuple(int(n) for n in indices.split(' '))
            problems.append((dimensions, indices))

    return presents, problems


def part1(presents: Presents, problems: List[Problem]) -> int:
    res = 0
    for problem in problems:
        if presents.problem_solvable(problem):
            res += 1
    return res


def main(test: bool):
    presents_, problems = get_input(test)
    presents = Presents(presents_)

    sum1 = part1(presents, problems)
    sum2 = 0

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [1,2]:
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
