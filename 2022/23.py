#!/usr/bin/env python
import os
import sys
import time
from collections import defaultdict

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> set[tuple[int, int]]:
    data = set()
    filename = 'inputs/23_test.txt' if test else 'inputs/23.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for y, line in enumerate(input_):
            for x, c in enumerate(line[:-1]):
                if c == '#':
                    data.add((x, y))
    return data


def print_state(state: set[tuple[int, int]], cnt: int) -> None:
    x_min = min(p[0] for p in state)
    y_min = min(p[1] for p in state)
    x_max = max(p[0] for p in state)
    y_max = max(p[1] for p in state)
    print('round', cnt)
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) in state:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


def calc_score_part1(data: set[tuple[int, int]]) -> int:
    x_min = min(p[0] for p in data)
    y_min = min(p[1] for p in data)
    x_max = max(p[0] for p in data)
    y_max = max(p[1] for p in data)
    res = 0
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) not in data:
                res += 1
    return res


def solve(data: set[tuple[int, int]]) -> tuple[int, int]:
    directions = ['N', 'S', 'W', 'E']
    direction_moves = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0)
    }
    direction_checks = {
        'N': [(-1, -1), (0, -1), (1, -1)],
        'S': [(-1, 1), (0, 1), (1, 1)],
        'W': [(-1, -1), (-1, 0), (-1, 1)],
        'E': [(1, -1), (1, 0), (1, 1)],
    }
    state = data
    sum1 = 0
    cnt = 0
    moved = True
    while moved:
        moved = False
        moves = {}
        # calc moves
        for x, y in state:
            direction = None
            # if the elf has no neighbors at all, it does not move
            if any(
                    (x + dx, y + dy) in state
                    for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                    if (dx, dy) != (0, 0)
            ):
                for i in range(cnt, cnt + 4):
                    test_direction = directions[i % 4]
                    if not any(
                            (x + direction_checks[test_direction][i][0],
                             y + direction_checks[test_direction][i][1]) in state for i in range(3)
                    ):
                        # can move
                        direction = test_direction
                        break
            if direction is None:
                # elf cannot move
                moves[(x, y)] = (x, y)
            else:
                moves[(x, y)] = (x + direction_moves[direction][0],
                                 y + direction_moves[direction][1])

        # move
        destinations_cnt = defaultdict(int)
        for dst in moves.values():
            destinations_cnt[dst] += 1
        next_state = set()
        for src, dst in moves.items():
            if src == dst:
                # elf does not move
                next_state.add(src)
            elif destinations_cnt[dst] > 1:
                # 2 elfes want to move to the same field
                # so, they do not move
                next_state.add(src)
            else:
                # elf moves
                moved = True
                next_state.add(dst)
        state = next_state
        cnt += 1
        # print_state(state, cnt)
        if cnt == 10:
            sum1 = calc_score_part1(state)
    return sum1, cnt


def main(test: bool):
    data = get_input(test)

    sum1, sum2 = solve(data)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    print('part2:', sum2)
    if sum1 not in [110, 3906]:
        raise WrongAnswer('part1')
    if sum2 not in [20, 895]:
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
