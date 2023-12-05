#!/usr/bin/env python
from __future__ import annotations

import time
import re
from typing import List


class Range:
    def __init__(self, start_dst: int, start_src: int, length: int):
        self.start = start_src
        self.end = start_src + length - 1
        self.offset = start_dst - start_src

    def __repr__(self):
        return f'<range [{self.start}, {self.end}] -> [{self.start + self.offset}, {self.end + self.offset}]'


class Converter:
    def __init__(self, name):
        self.name = name
        self.ranges: List[Range] = []

    def add_range(self, start_dst: int, start_src: int, length: int):
        self.ranges.append(Range(start_dst, start_src, length))

    def get_dst(self, value: int):
        for r in self.ranges:
            if r.start <= value <= r.end:
                return value + r.offset
        return value

    def __repr__(self):
        return f'<Conv {self.name}:{[str(r) for r in self.ranges]}>'


def get_input(test):
    data = []
    filename = 'inputs/05_test.txt' if test else 'inputs/05.txt'
    with open(filename, 'r') as file:
        input_ = file.read()[:-1].split('\n\n')
        seeds = [int(x) for x in input_[0].split(' ')[1:]]
        converters = dict()
        for entry in input_[1:]:
            lines = entry.split('\n')
            name = re.match(r"(.*) map:", lines[0]).groups()[0]
            converter = Converter(name)
            for numbers_str in lines[1:]:
                match = re.match(r"(\d+) (\d+) (\d+)", numbers_str)
                nums_str = match.groups()
                numbers = [int(x) for x in nums_str]
                converter.add_range(*numbers)

            converters[name] = converter

    return seeds, converters


def main(test):
    seeds, converters = get_input(test)

    conv = converters['seed-to-soil']
    soils = [conv.get_dst(s) for s in seeds]

    conv = converters['soil-to-fertilizer']
    ferts = [conv.get_dst(s) for s in soils]

    conv = converters['fertilizer-to-water']
    waters = [conv.get_dst(s) for s in ferts]

    conv = converters['water-to-light']
    light = [conv.get_dst(s) for s in waters]

    conv = converters['light-to-temperature']
    temperature = [conv.get_dst(s) for s in light]

    conv = converters['temperature-to-humidity']
    humidity = [conv.get_dst(s) for s in temperature]

    conv = converters['humidity-to-location']
    location = [conv.get_dst(s) for s in humidity]

    print(seeds)
    print(soils)
    print(ferts)
    print(waters)
    print(temperature)
    print(humidity)
    print(location)

if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    # main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
