#!/usr/bin/env python
import os
import sys
import time
from collections import deque

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[str]:
    data = []
    filename = 'inputs/20_test.txt' if test else 'inputs/20.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def get_start_and_end(data: list[str]) -> tuple[tuple[int, int], tuple[int, int]]:
    start = None
    end = None
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
    assert start is not None
    assert end is not None
    return start, end


def get_distances(data: list[str], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    todo = deque()
    todo.append((start, 0))
    dist = {start: 0}
    while todo:
        pos, cnt = todo.popleft()
        x, y = pos
        n_cnt = cnt + 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n_pos = (x + dx, y + dy)
            if data[n_pos[1]][n_pos[0]] != '#' and n_pos not in dist:
                dist[n_pos] = n_cnt
                todo.append((n_pos, n_cnt))
    return dist


def count_cheats(dist: dict[tuple[int, int], int], max_len: int, save: int) -> int:
    # a cheat leaves the track at one cell and rejoins it at another, moving max_len
    # steps through walls; the time saved is distance walked minus the shortcut
    res = 0
    for (x, y), cnt in dist.items():
        for dx in range(-max_len, max_len + 1):
            for dy in range(-(max_len - abs(dx)), max_len - abs(dx) + 1):
                if dx == 0 and dy == 0:
                    continue
                n_pos = (x + dx, y + dy)
                if n_pos in dist and dist[n_pos] - cnt - abs(dx) - abs(dy) >= save:
                    res += 1
    return res


def solve(data: list[str], max_len: int, save: int) -> int:
    start, _ = get_start_and_end(data)
    dist = get_distances(data, start)
    return count_cheats(dist, max_len, save)


def main(test: bool):
    data = get_input(test)

    # sample: part1 counts cheats saving >= 64, part2 cheats saving >= 50
    sum1 = solve(data, 2, 64 if test else 100)
    sum2 = solve(data, 20, 50 if test else 100)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [1, 1450]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [285, 1015247]:
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
