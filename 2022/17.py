from __future__ import annotations
import time
import re
from functools import cmp_to_key

import numpy as np


def get_input(test):
    filename = 'inputs/17_test.txt' if test else 'inputs/17.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()


def main(test):
    data = get_input(test)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
