#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[str]:
    data = []
    filename = 'inputs/24_test.txt' if test else 'inputs/24.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def parse_blocks(instructions: list[str]) -> list[tuple[int, int, int]]:
    # The 14 blocks are identical except for 3 constants:
    #   div z D   (D == 1  -> "push" block, D == 26 -> "pop" block)
    #   add x A   (the current digit must equal z % 26 + A)
    #   add y B   (if that check fails, digit + B is pushed onto z)
    blocks = []
    for i in range(0, len(instructions), 18):
        block = instructions[i:i + 18]
        D = int(block[4].split()[2])
        A = int(block[5].split()[2])
        B = int(block[15].split()[2])
        blocks.append((D, A, B))
    return blocks


def digit_pairs(blocks: list[tuple[int, int, int]]) -> dict[int, int]:
    # z is a base-26 stack. Push blocks always push, because their check can
    # never pass (A >= 10 > 9 >= digit). Pop blocks pop the top and compare the
    # digit against it. Pair every pop with the push it pops, in LIFO order.
    pairs = {}
    stack = []
    for i, (D, A, B) in enumerate(blocks):
        if D == 1:
            stack.append(i)
        else:
            pairs[stack.pop()] = i
    return pairs


def solve(blocks: list[tuple[int, int, int]], biggest: bool) -> int:
    # Each pop digit is tied to its push digit by one linear constraint:
    #   digit[pop] = digit[push] + B[push] + A[pop]
    # so the 14 digits split into 7 independent pairs. The push digit always
    # comes before its pop digit, so it is the more significant one: make it as
    # large (resp. small) as possible while its partner stays within 1..9.
    digits = [0] * 14
    order = range(9, 0, -1) if biggest else range(1, 10)
    for push, pop in digit_pairs(blocks).items():
        delta = blocks[push][2] + blocks[pop][1]
        for d in order:
            if 1 <= d + delta <= 9:
                digits[push] = d
                digits[pop] = d + delta
                break
        else:
            raise ValueError('no valid digit for a pair')
    return int(''.join(map(str, digits)))


def part1(instructions: list[str]) -> int:
    return solve(parse_blocks(instructions), biggest=True)


def part2(instructions: list[str]) -> int:
    return solve(parse_blocks(instructions), biggest=False)


def main(test: bool):
    data = get_input(test)

    sys.stdout = original_stdout  # enable print
    if len(data) != 14 * 18:
        print('skip: input is not a full MONAD program')
        return

    sum1 = part1(data)
    sum2 = part2(data)

    print('part1:', sum1)
    if sum1 not in [99429795993929]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [18113181571611]:
        raise WrongAnswer('part2')


if __name__ == '__main__':
    startTime = time.time()

    try:
        #print('Test')
        #main(True)
        print('real')
        sys.stdout = open(os.devnull, 'w')  # suppress test prints
        main(False)

    finally:
        executionTime = (time.time() - startTime)

        if executionTime < 60:
            print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
        else:
            print(f'Execution time: {round(executionTime, 3)} s')
