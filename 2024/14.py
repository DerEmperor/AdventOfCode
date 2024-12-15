#!/usr/bin/env python
from __future__ import annotations

import re
import time

'''
+---> x
|
|
v
y
'''

re_input = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: Pos):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)


class Robot:
    dimensions: Pos = None

    def __init__(self, pos: Pos, vel: Pos):
        self.pos = pos
        self.vel = vel

    def step(self):
        self.pos.x = (self.pos.x + self.vel.x) % self.dimensions.x
        self.pos.y = (self.pos.y + self.vel.y) % self.dimensions.y

    def __repr__(self):
        return f'<{self.pos}, {self.vel}>'


def get_input(test: bool):
    data = []
    filename = 'inputs/14_test.txt' if test else 'inputs/14.txt'
    with open(filename, 'r') as file:
        input_ = file.read()
    for match in re_input.finditer(input_):
        px, py, vx, vy = [int(x) for x in match.groups()]
        data.append(Robot(Pos(px, py), Pos(vx, vy)))
    Robot.dimensions = Pos(101, 103) if not test else Pos(11, 7)
    return data


def get_safety(robots: list[Robot]):
    quad_tl = 0
    quad_tr = 0
    quad_bl = 0
    quad_br = 0

    for robot in robots:
        if robot.pos.x < robot.dimensions.x // 2:
            if robot.pos.y < robot.dimensions.y // 2:
                quad_tl += 1
            elif robot.pos.y > robot.dimensions.y // 2:
                quad_bl += 1
        elif robot.pos.x > robot.dimensions.x // 2:
            if robot.pos.y <= robot.dimensions.y // 2:
                quad_tr += 1
            elif robot.pos.y > robot.dimensions.y // 2:
                quad_br += 1
    return quad_bl * quad_br * quad_tr * quad_tl


def draw_robots(positions):
    res = []
    for y in range(Robot.dimensions.y):
        res.append([' '] * Robot.dimensions.x)
    for x, y in positions:
        res[y][x] = '#'

    with open('out_14.txt', 'w') as file:
        for line in res:
            file.write(''.join(line) + '\n')



def main(test: bool):
    robots = get_input(test)

    min_score = float('inf')
    positions = None
    i=0
    min_i=None
    while True:
        for _ in range(1000):
            for robot in robots:
                robot.step()
            i += 1
            score = get_safety(robots)
            if score < min_score:
                min_score = score
                min_i = i
                positions = [(r.pos.x, r.pos.y) for r in robots]
            if i == 100:
                print('part1:', get_safety(robots))
        draw_robots(positions)
        input_ = input(f'seconds: {min_i}. stop?[y/n]').lower()
        while input_ not in ['y', 'n']:
            input_ = input(f'seconds: {min_i}. stop?[y/n]. Type "y" or "n".').lower()
        if input_ == 'y':
            break

if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    #main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
