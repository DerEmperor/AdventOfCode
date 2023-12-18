#!/usr/bin/env python
from __future__ import annotations
import time
from functools import cached_property
from itertools import groupby
from typing import List

CARDS1 = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
CARDS2 = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}


def _get_value(cards: str, part1: bool) -> int:
    CARDS = CARDS1 if part1 else CARDS2
    res = _first_rank(cards, part1) * 16 ** 5
    res += CARDS[cards[0]] * 16 ** 4
    res += CARDS[cards[1]] * 16 ** 3
    res += CARDS[cards[2]] * 16 ** 2
    res += CARDS[cards[3]] * 16 ** 1
    res += CARDS[cards[4]]
    return res


def _first_rank(cards: str, part1: bool) -> int:
    s = set(cards)
    if not part1 and 'J' in s:
        if cards == 'JJJJJ':
            return 7
        res = 0
        for c in (s - {'J'}):
            new_cards = cards.replace('J', c)
            res = max(res, _first_rank(new_cards, True))
        return res

    length = len(s)

    if length == 5:
        # highest card
        return 1
    elif length == 4:
        # 1 pair
        return 2
    elif length == 1:
        # quint
        return 7
    if length == 3:
        # 2 pairs or triple
        for c in s:
            cnt = cards.count(c)
            if cnt == 3:
                # triple
                return 4
            if cnt == 2:
                # 2 pairs
                return 3
    elif length == 2:
        # full house or quad
        cnt = cards.count(cards[0])
        if cnt in {1, 4}:
            # quad
            return 6
        elif cnt in {2, 3}:
            # full house
            return 5

    assert False


class Hand:
    def __init__(self, cards: str, bet: str):
        self.cards = cards
        self.bet = int(bet)
        self.value1 = _get_value(cards, True)
        self.value2 = _get_value(cards, False)

    def __repr__(self):
        return f'<{self.cards} {hex(self.value1)} {hex(self.value2)} {self.bet}>'


def get_input(test: bool) -> List[Hand]:
    data = []
    filename = 'inputs/07_test.txt' if test else 'inputs/07.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            hand, bet = line[:-1].split()
            data.append(Hand(hand, bet))

    return data


def main(test: bool):
    hands = get_input(test)
    hands = sorted(hands, key=lambda h: h.value1)
    sum1 = 0
    for rank, hand in enumerate(hands, 1):
        sum1 += rank * hand.bet

    hands = sorted(hands, key=lambda h: h.value2)
    sum2 = 0
    for rank, hand in enumerate(hands, 1):
        sum2 += rank * hand.bet

    print(sum1, sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
