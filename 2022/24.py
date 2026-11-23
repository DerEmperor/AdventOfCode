#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


t_blizzards = dict[str, set[tuple[int, int]]]


def get_input(test: bool) -> tuple[t_blizzards, int, int]:
    blizzards = {
        '>': set(),
        '<': set(),
        'v': set(),
        '^': set(),
    }
    filename = 'inputs/24_test.txt' if test else 'inputs/24.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for y, line in enumerate(input_):
            for x, c in enumerate(line):
                if c in blizzards:
                    blizzards[c].add((x, y))
        n = len(input_[0].rstrip())
        m = len(input_)
    return blizzards, n, m


DIRECTIONS = {
    'v': (0, 1),
    '^': (0, -1),
    '<': (-1, 0),
    '>': (1, 0),
}


def advance_blizzards(blizzards: t_blizzards, n: int, m: int) -> t_blizzards:
    res = {}
    for direction, blizzard_chunk in blizzards.items():

        new = set()
        for x, y in blizzard_chunk:
            dx, dy = DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            if nx <= 0:
                nx = n - 2
            elif nx >= n - 1:
                nx = 1
            elif ny <= 0:
                ny = m - 2
            elif ny >= m - 1:
                ny = 1
            new.add((nx, ny))
        res[direction] = new

    return res


def navigate(
        blizzards: t_blizzards,
        n: int,
        m: int,
        start:tuple[int, int],
        goal: tuple[int, int],
) -> tuple[t_blizzards, int]:
    todo = {start}
    minute = 0
    while True:
        next_todo = set()
        for pos in todo:
            if pos == goal:
                return blizzards, minute
            if any(pos in b for b in blizzards.values()):
                # we are in a blizzards, that is illegal
                continue
            # move
            x, y = pos
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]:
                nx, ny = x + dx, y + dy
                if ((
                        1 <= nx <= n - 2 and 1 <= ny <= m - 2)
                        or (nx, ny) == goal or (nx, ny) == start
                ):
                    # inner area plus both border cells (entrance and exit), in every leg
                    next_todo.add((nx, ny))
        blizzards = advance_blizzards(blizzards, n, m)
        todo = next_todo
        minute += 1


def solve(blizzards: t_blizzards, n: int, m: int) -> tuple[int, int]:
    start =(1, 0)
    goal = (n - 2, m - 1)
    blizzards, part1 = navigate(blizzards, n, m, start, goal)
    part2 = part1
    blizzards, tmp = navigate(blizzards, n, m, goal, start)
    part2 += tmp
    _, tmp = navigate(blizzards, n, m, start, goal)
    part2 += tmp
    return part1, part2


def main(test: bool):
    blizzards, n, m = get_input(test)

    sum1, sum2 = solve(blizzards, n, m)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [18, 242]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [54, 720]:
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
