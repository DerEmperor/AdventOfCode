from __future__ import annotations

import time
from typing import Tuple, List


def get_input(test: bool) -> List[Tuple[str, str]]:
    filename = 'inputs/03_test.txt' if test else 'inputs/03.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    res = []
    for line in input_:
        l = len(line) - 1
        assert l % 2 == 0
        a = line[:l // 2]
        b = line[l // 2:-1]
        res.append((a, b))
    return res


def main(test):
    data = get_input(test)
    score = 0
    for a, b in data:
        char = (set(a) & set(b)).pop()
        assert len(set(a) & set(b)) == 1
        char_score = ord(char) - ord('a') + 1 if ord(char) >= ord('a') else ord(char) - ord('A') + 27
        score += char_score

    data = [a + b for a, b in data]
    groups = []
    for i in range(0, len(data), 3):
        a, b, c = data[i:i + 3]
        groups.append((a, b, c))

    score2 = 0
    for a, b, c in groups:
        char = (set(a) & set(b) & set(c)).pop()
        assert len(set(a) & set(b) & set(c)) == 1
        char_score = ord(char) - ord('a') + 1 if ord(char) >= ord('a') else ord(char) - ord('A') + 27
        score2 += char_score

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
