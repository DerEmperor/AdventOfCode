from __future__ import annotations

import time
from typing import Tuple, List

scores = {
    ('A', 'X'): 3 + 1,
    ('A', 'Y'): 6 + 2,
    ('A', 'Z'): 0 + 3,
    ('B', 'X'): 0 + 1,
    ('B', 'Y'): 3 + 2,
    ('B', 'Z'): 6 + 3,
    ('C', 'X'): 6 + 1,
    ('C', 'Y'): 0 + 2,
    ('C', 'Z'): 3 + 3,
}

scores2 = {
    ('A', 'X'): scores[('A', 'Z')],
    ('A', 'Y'): scores[('A', 'X')],
    ('A', 'Z'): scores[('A', 'Y')],
    ('B', 'X'): scores[('B', 'X')],
    ('B', 'Y'): scores[('B', 'Y')],
    ('B', 'Z'): scores[('B', 'Z')],
    ('C', 'X'): scores[('C', 'Y')],
    ('C', 'Y'): scores[('C', 'Z')],
    ('C', 'Z'): scores[('C', 'X')],
}


def get_input(test: bool) -> List[Tuple[str, str]]:
    filename = 'inputs/02_test.txt' if test else 'inputs/02.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    res = []
    for a, _, c, _ in input_:
        res.append((a, c))
    return res


def main(test):
    data = get_input(test)
    score = 0
    score2 = 0
    for a, b in data:
        score += scores[(a, b)]
        score2 += scores2[(a, b)]
    print(score)
    print(score2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
