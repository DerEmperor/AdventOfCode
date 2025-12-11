#!/usr/bin/env python
import os
import sys
import time
from functools import cache, lru_cache
from typing import List, Dict, Tuple, Set

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool, cnt: str = '') -> Dict[str, List[str]]:
    devices = {}
    filename = f'inputs/11_test{cnt}.txt' if test else 'inputs/11.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            device, outputs = line[:-1].split(': ')
            devices[device] = outputs.split(' ')
    return devices


def dfs(devices: Dict[str, List[str]], current_device: str, end_device: str) -> int:
    @cache
    def dfs_helper(current_device_inner: str) -> int:
        if current_device_inner == end_device:
            return 1
        res = 0
        for next_devices in devices.get(current_device_inner, []):
            res += dfs_helper(next_devices)
        return res

    return dfs_helper(current_device)


def part1(devices: Dict[str, List[str]]):
    return dfs(devices, 'you', 'out')


def part2(devices: Dict[str, List[str]]):
    # fft is always before dac
    dac_out = dfs(devices, 'dac', 'out')
    fft_dac = dfs(devices, 'fft', 'dac')
    svr_fft = dfs(devices, 'svr', 'fft')

    return svr_fft * fft_dac * dac_out


def main(test: bool):
    devices = get_input(test)

    sum1 = part1(devices)
    if test:
        devices = get_input(test, '2')
    sum2 = part2(devices)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [5, 523]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [2, 517315308154944]:
        raise WrongAnswer('part2')


if __name__ == '__main__':
    startTime = time.time()

    try:
        print('Test')
        main(True)
        print('real')
        sys.stdout = open(os.devnull, 'w')  # suppress test prints
        main(False)

    finally:
        executionTime = (time.time() - startTime)

        if executionTime < 60:
            print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
        else:
            print(f'Execution time: {round(executionTime, 3)} s')
