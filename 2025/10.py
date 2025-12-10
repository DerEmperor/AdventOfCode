#!/usr/bin/env python
import os
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple

from z3 import Optimize, Int, Sum, sat

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


@dataclass
class Machine:
    lights: int
    """msb is light 0, always start with 1 to prevent cutoff"""
    buttons: List[Tuple[int]]
    joltage: List[int]

    @classmethod
    def from_data(cls, line: str) -> Machine:
        parts = line.split(' ')
        lights_str = parts[0]
        buttons_str = parts[1:-1]
        joltage_str = parts[-1]
        lights_binary_str = '1' + ''.join(['1' if c == '#' else '0' for c in lights_str[1:-1]])[::-1]
        lights = int(lights_binary_str, base=2)
        joltage = [int(j) for j in joltage_str[1:-1].split(',')]
        buttons = []
        for b in buttons_str:
            buttons.append(tuple(int(x) for x in b[1:-1].split(',')))

        return cls(lights, buttons, joltage)

    def __repr__(self):
        return f'<{bin(self.lights)[:2:-1]}, {self.buttons}, {self.joltage}>'


def get_input(test: bool) -> List[Machine]:
    data = []
    filename = 'inputs/10_test.txt' if test else 'inputs/10.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(Machine.from_data(line[:-1]))
    return data


def press_button(lights: int, button: Tuple[int]) -> int:
    mask = 0
    for i in button:
        mask |= 1 << i
    return lights ^ mask


def part1(machine: Machine) -> int:
    todo = [(1 << machine.lights.bit_length() - 1, 0)]  # start with all 0, but keep 1 as start
    visited = set()
    while todo:
        lights, cnt = todo.pop(0)
        if lights == machine.lights:
            return cnt
        for b in machine.buttons:
            toggled_lights = press_button(lights, b)
            if toggled_lights not in visited:
                visited.add(toggled_lights)
                todo.append((toggled_lights, cnt + 1))

    raise Exception(f'no solution for machine: {machine}')


def part2(machine: Machine) -> int:
    """stolen from https://github.com/nitekat1124/advent-of-code-2025/blob/main/solutions/day10.py"""
    # use z3 optimizer in order to get the minimal presses
    opt = Optimize()
    press_counts = [Int(f"cnt_{i}") for i in range(len(machine.buttons))]

    # button press count must >= 0
    for count in press_counts:
        opt.add(count >= 0)

    # pick which button affects which joltage index
    for pos, joltage in enumerate(machine.joltage):
        affects = [press_counts[idx] for idx, btn in enumerate(machine.buttons) if pos in btn]
        opt.add(Sum(affects) == joltage)

    # minimize total presses
    opt.minimize(Sum(press_counts))

    if opt.check() == sat:
        model = opt.model()
        return sum(model[c].as_long() for c in press_counts)
    else:
        raise ValueError("No solution found")

def main(test: bool):
    machines = get_input(test)

    sum1 = 0
    sum2 = 0

    for machine in machines:
        sum1 += part1(machine)
        sum2 += part2(machine)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [7, 520]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [33, 20626]:
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
