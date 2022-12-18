from __future__ import annotations
import time
import re
from functools import cmp_to_key

import numpy as np


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def as_tuple(self):
        return self.x, self.y

    @staticmethod
    def dis(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def dis_to(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


class Sensor:
    def __init__(self, pos_x, pos_y, beacon_x, beacon_y):
        self.pos = Coord(pos_x, pos_y)
        self.beacon = Coord(beacon_x, beacon_y)
        self.distance = Coord.dis(self.pos, self.beacon)

    def __repr__(self):
        return f'<S: {self.pos}, {self.beacon}, {self.distance}>'

    def walk_frame(self):
        # upper right:
        y = self.pos.y + self.distance + 1
        for x in range(self.pos.x, self.pos.x + self.distance + 1, 1):
            yield x, y
            y -= 1

        # lower right:
        for x in range(self.pos.x + self.distance + 1, self.pos.x, -1):
            yield x, y
            y -= 1

        # lower left:
        for x in range(self.pos.x, self.pos.x - self.distance - 1, -1):
            yield x, y
            y += 1

        # upper left:
        for x in range(self.pos.x - self.distance - 1, self.pos.x, 1):
            yield x, y
            y += 1


def get_input(test):
    filename = 'inputs/15_test.txt' if test else 'inputs/15.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)\n')

    sensors = []
    for line in input_:
        match = regex.match(line)
        assert match
        poss = [int(i) for i in match.groups()]
        sensor = Sensor(*poss)
        sensors.append(sensor)

    return sensors


def part1(test):
    sensors = get_input(test)
    y = 10 if test else 2000000
    points = set()
    for sensor in sensors:
        # |x - sensor_x | + | y - sensor_y| <= sensor_beacon_distance -> no_beacon here
        # solve for x
        # x >= - sensor_beacon_distance + | y - sensor_y| + sensor_x   assert x <= sensor_x
        x_min = -sensor.distance + abs(y - sensor.pos.y) + sensor.pos.x

        # x <= sensor_beacon_distance - | y - sensor_y| + sensor_x    assert x > sensor_x
        x_max = sensor.distance - abs(y - sensor.pos.y) + sensor.pos.x

        if (x_max >= x_min):
            r = range(x_min, x_max + 1)
            cur_points = set(r)
            if sensor.beacon.y == y:
                cur_points.discard(sensor.beacon.x)
            points = points | cur_points

    score1 = len(points)
    print(score1)


def part2(test):
    sensors = get_input(test)
    size = (0, 20 if test else 4000000, 0, 20 if test else 4000000)
    for sensor in sensors:
        for x, y in sensor.walk_frame():
            # missing beacon must be here
            if not (size[0] <= x <= size[1] and size[2] <= y <= size[3]):
                continue
            this_is_the_spot = True
            for sensor2 in sensors:
                if sensor is sensor2:
                    continue
                if sensor2.pos.dis_to(x, y) <= sensor2.distance:
                    this_is_the_spot = False
                    break
            if this_is_the_spot:
                print(x, y, x * 4000000 + y)
                return


def main(test):
    print('part 1:')
    part1(test)
    print()
    print('part 2:')
    part2(test)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print()
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
