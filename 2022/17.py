from __future__ import annotations
import time

# TODO classes for blocks

B_MINUS = [
    '####',
]
B_PLUS = [
    '.#.',
    '###',
    '.#.',
]

B_L = [
    '..#',
    '..#',
    '###',
]
B_I = [
    '#'
    '#'
    '#'
    '#'
]
B_O = [
    '##',
    '##',
]


class Iter:
    def __init__(self, sequence):
        self.sequence = sequence
        self.pnt = 0
        self.l = len(self.sequence)

    def __iter__(self):
        return self

    def __next__(self):
        res = self.sequence[self.pnt]
        self.pnt = (self.pnt + 1) % self.l
        return res


def get_input(test):
    filename = 'inputs/17_test.txt' if test else 'inputs/17.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return input_[0]


def main(test):
    data = get_input(test)
    blocks = [B_MINUS, B_PLUS, B_L, B_I, B_O]
    block_iter = Iter(blocks)
    jet_iter = Iter(data)
    floor_height = [0] * 7

    for block in blocks:


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    # print('real')
    # main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 10:
        print(f'Execution time: {round(executionTime, 3)} s')

    else:
        print(f'Execution time: {round(executionTime * 1000, 3)} ms')
