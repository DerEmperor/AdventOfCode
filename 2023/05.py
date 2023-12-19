#!/usr/bin/env python
from __future__ import annotations

import time
import re
from typing import List, Tuple


class Range:
    def __init__(self, start_dst: int, start_src: int, length: int):
        # end inclusive
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
        self.ranges = sorted(self.ranges, key=lambda r: r.start)

    def get_dst(self, value: int | Tuple[int, int]) -> List[int | Tuple[int, int]]:
        if isinstance(value, int):
            for r in self.ranges:
                if r.start <= value <= r.end:
                    return [value + r.offset]
            return [value]

        else:
            start, end = value
            for r in self.ranges:
                if r.start <= start <= r.end:
                    if end <= r.end:
                        return [(start + r.offset, end + r.offset)]
                    else:
                        return [(start + r.offset, r.end + r.offset)] + self.get_dst((r.end + 1, end))
                elif start < r.start:
                    if end < r.start:
                        return [(start, end)]
                    else:
                        return [(start, r.start - 1)] + self.get_dst((r.start, end))

            return [(start, end)]

    def __repr__(self):
        return f'<Conv {self.name}:{[str(r) for r in self.ranges]}>'


def get_input(test):
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


def convert(seeds, converters):
    print('seeds:', seeds)
    conv = converters['seed-to-soil']
    soils = []
    for s in seeds:
        soils.extend(conv.get_dst(s))
    print('soils', soils)

    conv = converters['soil-to-fertilizer']
    ferts = []
    for s in soils:
        ferts.extend(conv.get_dst(s))
    print('ferts', ferts)

    conv = converters['fertilizer-to-water']
    waters = []
    for s in ferts:
        waters.extend(conv.get_dst(s))
    print('waters', waters)

    conv = converters['water-to-light']
    light = []
    for s in waters:
        light.extend(conv.get_dst(s))
    print('light', light)

    conv = converters['light-to-temperature']
    temperature = []
    for s in light:
        temperature.extend(conv.get_dst(s))
    print('temperature', temperature)

    conv = converters['temperature-to-humidity']
    humidity = []
    for s in temperature:
        humidity.extend(conv.get_dst(s))
    print('humidity', humidity)

    conv = converters['humidity-to-location']
    location = []
    for s in humidity:
        location.extend(conv.get_dst(s))
    print('location', location)

    return location


def main(test):
    seeds, converters = get_input(test)
    print(min(convert(seeds, converters)))

    seeds2 = []
    for start, length in zip(seeds[::2], seeds[1::2]):
        seeds2.append((start, start + length - 1))
    res = convert(seeds2, converters)
    for start, end in res:
        assert start <= end
    print(min(start for start, end in res))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
