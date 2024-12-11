#!/usr/bin/env python
import time
from collections import defaultdict


def get_input(test: bool):
    data = defaultdict(int)
    filename = 'inputs/11_test.txt' if test else 'inputs/11.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    for x in input_[0][:-1].split(' '):
        data[int(x)] += 1
    return data


def main(test: bool):
    stones = get_input(test)

    for i, end in enumerate([25, 50], 1):
        for _ in range(end):
            new_stones = defaultdict(int)
            for stone, num in stones.items():
                if stone == 0:
                    new_stones[1] += num
                elif (stone_str := str(stone)) and len(stone_str) % 2 == 0:
                    half = len(stone_str) // 2
                    new_stones[int(stone_str[:half])] += num
                    new_stones[int((stone_str[half:].lstrip('0')) or '0')] += num
                else:
                    new_stones[stone * 2024] += num
            stones = new_stones

        print(f'part {i}:', sum(num for num in stones.values()))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
