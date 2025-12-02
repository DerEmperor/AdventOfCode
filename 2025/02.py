#!/usr/bin/env python
import re
import time
from typing import List, Tuple

re_part2 = re.compile(r'(.+)\1+')

def get_input(test: bool) -> List[Tuple[int, int]]:
    data = []
    filename = 'inputs/02_test.txt' if test else 'inputs/02.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for id_range in input_[0][:-1].split(','):
            data.append(tuple(int(x) for x in id_range.split('-')))
    return data


def is_invalid_id(num: int) -> bool:
    num = str(num)
    return num[:len(num)//2] == num[len(num)//2:]

def is_invalid_id_part2(num: int) -> bool:
    return re_part2.fullmatch(str(num)) is not None


def main(test: bool):
    data = get_input(test)

    sum1 = 0
    sum2 = 0

    for start, end in data:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                sum1 += num
            if is_invalid_id_part2(num):
                sum2 += num

    print('part1:', sum1)
    print('part2:', sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)

    if executionTime < 60:
        print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
    else:
        print(f'Execution time: {round(executionTime, 3)} s')
