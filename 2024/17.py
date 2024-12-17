#!/usr/bin/env python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


class Computer:
    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c
        self.program = program
        self.ip = 0  # instruction pointer
        self.halted = False
        self.stdout = []

        self.instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        self.combo = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: lambda: self.reg_a,
            5: lambda: self.reg_b,
            6: lambda: self.reg_c,
            7: lambda: 1 / 0,
        }

    def adv(self, x: int):
        self.reg_a = self.reg_a >> self.combo[x]()

    def bxl(self, x: int):
        self.reg_b = self.reg_b ^ x

    def bst(self, x: int):
        self.reg_b = self.combo[x]() % 8

    def jnz(self, x: int):
        if self.reg_a != 0:
            self.ip = x - 2

    def bxc(self, x: int):
        # x not used
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, x: int):
        self.stdout.append(self.combo[x]() % 8)

    def bdv(self, x: int):
        self.reg_b = self.reg_a >> self.combo[x]()

    def cdv(self, x: int):
        self.reg_c = self.reg_a >> self.combo[x]()

    def run(self):
        while not self.halted:
            instruction = self.instructions[self.program[self.ip]]
            operand = self.program[self.ip + 1]
            instruction(operand)
            self.ip += 2
            if self.ip >= len(self.program):
                self.halted = True


def get_input(test: bool):
    filename = 'inputs/17_test_2.txt' if test else 'inputs/17.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    data = [
        int(input_[0][12:-1]),
        int(input_[1][12:-1]),
        int(input_[2][12:-1]),
        [int(x) for x in input_[4][9:-1].split(',')]
    ]
    return data


def solve(p, r, g):
    """https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2gizvj/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"""
    if p < 0:
        print('part2:', r)
        return True
    for d in range(8):
        a, i = r << 3 | d, 0
        while i < len(g):
            if g[i + 1] <= 3:
                o = g[i + 1]
            elif g[i + 1] == 4:
                o = a
            elif g[i + 1] == 5:
                o = b
            elif g[i + 1] == 6:
                o = c
            if g[i] == 0:
                a >>= o
            elif g[i] == 1:
                b ^= g[i + 1]
            elif g[i] == 2:
                b = o & 7
            elif g[i] == 3:
                i = g[i + 1] - 2 if a != 0 else i
            elif g[i] == 4:
                b ^= c
            elif g[i] == 5:
                w = o & 7; break
            elif g[i] == 6:
                b = a >> o
            elif g[i] == 7:
                c = a >> o
            i += 2
        if w == g[p] and solve(p - 1, r << 3 | d, g):
            return True
    return False


def main(test: bool):
    a, b, c, p = get_input(test)
    computer = Computer(a, b, c, p)
    computer.run()
    print('part1:', ','.join(str(x) for x in computer.stdout))

    solve(len(p) - 1, 0, p)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    # main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
