#!/usr/bin/env python
import os
import sys
import time
from collections import defaultdict

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> dict[str, set[str]]:
    data = defaultdict(set)
    filename = 'inputs/23_test.txt' if test else 'inputs/23.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            a, b = line.strip().split('-')
            data[a].add(b)
            data[b].add(a)
    return data


def part1(cons: dict[str, set[str]]) -> int:
    res = 0
    for a in cons:
        for b in cons[a]:
            if b < a:
                # count every pair only once
                continue
            for c in cons[a] & cons[b]:
                if c < b:
                    continue
                if a.startswith('t') or b.startswith('t') or c.startswith('t'):
                    # 3 mutually connected computers, one name starting with t
                    res += 1
    return res


def part2(cons: dict[str, set[str]]) -> str:
    """Bron–Kerbosch algorithm"""
    best = []

    def grow(clique: list[str], candidates: set[str], excluded: set[str]) -> None:
        nonlocal best
        if not candidates and not excluded:
            # nobody can join anymore: the clique is maximal
            if len(clique) > len(best):
                best = clique.copy()
            return
        for c in list(candidates):  # snapshot: we mutate the sets below
            grow(clique + [c], candidates & cons[c], excluded & cons[c])
            # from now on, c may only appear in groups found via earlier branches
            candidates.remove(c)
            excluded.add(c)

    grow([], set(cons), set())
    return ','.join(sorted(best))


def main(test: bool):
    cons = get_input(test)

    sum1 = part1(cons)
    sum2 = part2(cons)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [7, 1467]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in ['co,de,ka,ta', 'di,gs,jw,kz,md,nc,qp,rp,sa,ss,uk,xk,yn']:
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
