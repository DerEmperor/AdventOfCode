from __future__ import annotations
from typing import List, Tuple, Dict
import time
import re
import sys


class D100Determ:
    def __init__(self):
        self.counter = 0

    def roll(self) -> int:
        res = self.counter % 100
        self.counter += 1
        return res + 1


def get_input(test: bool) -> Tuple[int, int]:
    filename = 'inputs/21_input_test.txt' if test else 'inputs/21_input.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    start_1 = input_[0][28]
    start_2 = input_[1][28]

    return int(start_1), int(start_2)


def main():
    print('Test')
    pos1, pos2 = get_input(True)
    part1(pos1, pos2)
    part2(pos1, pos2)
    print('real')
    pos1, pos2 = get_input(False)
    part1(pos1, pos2)
    part2(pos1, pos2)


def part1(pos1: int, pos2: int) -> None:
    dice = D100Determ()
    pos = [pos1, pos2]
    scores = [0, 0]
    player = 0
    while scores[0] < 1000 and scores[1] < 1000:
        roll = dice.roll() + dice.roll() + dice.roll()
        pos[player] = (pos[player] + roll - 1) % 10 + 1
        scores[player] += pos[player]
        player = (player + 1) % 2
        # print('roll:', roll, 'pos:', pos, 'scores:', scores)

    print('scores:', scores, 'dice counter', dice.counter, 'solution', min(scores) * dice.counter)


mem: Dict[Tuple[int, int, int, int], Tuple[int, int]] = dict()


def part2(pos1: int, pos2: int) -> None:
    wins = part2_helper(0, 0, pos1, pos2)

    print('wins:', wins, 'solution', max(wins))


def part2_helper(score0: int, score1: int, pos0: int, pos1: int) -> Tuple[int, int]:
    # base case
    if score0 >= 21:
        return 1, 0

    if score1 >= 21:
        return 0, 1

    if (score0, score1, pos0, pos1) in mem:
        return mem[(score0, score1, pos0, pos1)]

    ans = [0, 0]
    for roll1 in range(1, 4):
        for roll2 in range(1, 4):
            for roll3 in range(1, 4):
                roll = roll1 + roll2 + roll3
                new_pos0 = (pos0 + roll - 1) % 10 + 1
                new_score0 = score0 + new_pos0
                w0, w1 = part2_helper( score1, new_score0,pos1,new_pos0)

                ans[0] += w1
                ans[1] += w0
    mem[(score0, score1, pos0, pos1)] = (ans[0], ans[1])
    return ans[0], ans[1]


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
