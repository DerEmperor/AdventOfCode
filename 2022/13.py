from __future__ import annotations
import time
import re
from functools import cmp_to_key

import numpy as np


def get_input(test):
    filename = 'inputs/13_test.txt' if test else 'inputs/13.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    input_.append('\n')

    data = []
    for i in range(0, len(input_), 3):
        a, b, c = input_[i:i + 3]
        assert c == '\n'
        a = eval(a[:-1])
        b = eval(b[:-1])
        data.append((a, b))
    return data


def right_order(a, b) -> bool | None:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return True
        elif a > b:
            return False
        else:
            return None

    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            if i >= len(a):
                return True
            if i >= len(b):
                return False
            res = right_order(a[i], b[i])
            if res is not None:
                return res
        return None

    elif isinstance(a, list) and isinstance(b, int):
        return right_order(a, [b])

    elif isinstance(a, int) and isinstance(b, list):
        return right_order([a], b)

    else:
        raise Exception('Unreachable Code')


def compare(a, b):
    res = right_order(a, b)
    assert res is not None
    return 1 if res else -1


def main(test):
    data = get_input(test)
    score = 0
    for i, (a, b) in enumerate(data, 1):
        if compare(a, b) > 0:
            score += i

    print('part 1:', score)

    new_data = [[[2]], [[6]]]
    for a, b in data:
        new_data.append(a)
        new_data.append(b)

    sorted_data = sorted(new_data, key=cmp_to_key(compare), reverse=True)
    score2 = (sorted_data.index([[2]]) + 1) * (sorted_data.index([[6]]) + 1)
    print('part 2:', score2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
