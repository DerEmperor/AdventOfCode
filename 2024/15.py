#!/usr/bin/env python
from __future__ import annotations

import time
from enum import Enum
from itertools import cycle
from typing import List, Tuple
from unittest import case


class Tile(Enum):
    WALL = '#'
    BOX = 'O'
    BOX_L = '['
    BOX_R = ']'
    EMPTY = '.'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


directions = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


def get_input(test: bool):
    warehouse = []
    robot = None
    moves = []
    filename = 'inputs/15_test_2.txt' if test else 'inputs/15.txt'
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            warehouse.append([])
            if line == '\n':
                del warehouse[-1]
                break
            for x, char in enumerate(line[:-1]):
                if char == '@':
                    robot = (x, y)
                    warehouse[-1].append(Tile.EMPTY)
                else:
                    warehouse[-1].append(Tile(char))
        for line in file:
            for c in line[:-1]:
                moves.append(directions[c])
    return warehouse, robot, moves


def print_warehouse(warehouse, robot, i=None, dx=None, dy=None):
    for y, line in enumerate(warehouse):
        for x, t in enumerate(line):
            if (x, y) == robot:
                print('@', end='')
            else:
                print(t, end='')
        print()

    if i is not None:
        if dx == 0:
            if dy == -1:
                print(f'{i} ^')
            else:
                print(f'{i} v')
        elif dx == -1:
            print(f'{i} <')
        else:
            print(f'{i} >')
    else:
        print()


def part1(warehouse, robot, moves):
    # print_warehouse(warehouse, robot)
    dimensions = (len(warehouse[0]), len(warehouse))
    for dx, dy in moves:
        x, y = robot
        assert 0 <= x < dimensions[0] and 0 <= y < dimensions[1]
        nx, ny = x + dx, y + dy
        match warehouse[ny][nx]:
            case Tile.WALL:
                # do nothing
                pass
            case Tile.EMPTY:
                robot = (nx, ny)
            case Tile.BOX:
                while warehouse[ny][nx] == Tile.BOX:
                    nx += dx
                    ny += dy

                match warehouse[ny][nx]:
                    case Tile.WALL:
                        # do nothing
                        pass
                    case Tile.EMPTY:
                        robot = (x + dx, y + dy)
                        warehouse[y + dy][x + dx] = Tile.EMPTY
                        warehouse[ny][nx] = Tile.BOX
                    case Tile.BOX:
                        raise Exception('impossible')
        # print(dx, dy)
        # print_warehouse(warehouse, robot)

    score = 0
    for y, line in enumerate(warehouse):
        for x, t in enumerate(line):
            if t == Tile.BOX:
                score += 100 * y + x
    print('part1:', score)


def is_movable(warehouse: List[List[Tile]], x: int, y: int, dy: int) -> bool:
    match warehouse[y + dy][x]:
        case Tile.WALL:
            return False
        case Tile.EMPTY:
            return True
        case Tile.BOX_R:
            return (
                    is_movable(warehouse, x, y + dy, dy) and
                    is_movable(warehouse, x - 1, y + dy, dy)
            )
        case Tile.BOX_L:
            return (
                    is_movable(warehouse, x, y + dy, dy) and
                    is_movable(warehouse, x + 1, y + dy, dy)
            )
        case _:
            raise Exception('impossible')


def move_boxes(warehouse: List[List[Tile]], x: int, y: int, dy: int):
    # move box ahead first
    match warehouse[y + dy][x]:
        case Tile.WALL:
            raise Exception(f'impossible {x} {y + dy}')

        case Tile.EMPTY:
            pass

        case Tile.BOX_R | Tile.BOX_L:
            dx = 1 if warehouse[y + dy][x] == Tile.BOX_L else -1
            move_boxes(warehouse, x, y + dy, dy)
            move_boxes(warehouse, x + dx, y + dy, dy)

            assert warehouse[y + 2 * dy][x] == Tile.EMPTY, f'{x} {y + 2 * dy} {warehouse[y + 2 * dy][x]}'
            assert warehouse[y + 2 * dy][x + dx] == Tile.EMPTY, f'{x + dx} {y + 2 * dy} {warehouse[y + 2 * dy][x + dx]}'
            warehouse[y + 2 * dy][x] = warehouse[y + dy][x]
            warehouse[y + 2 * dy][x + dx] = warehouse[y + dy][x + dx]
            warehouse[y + dy][x] = Tile.EMPTY
            warehouse[y + dy][x + dx] = Tile.EMPTY

        case _:
            raise Exception('impossible')


def part2(warehouse, robot, moves):
    dimensions = (len(warehouse[0]), len(warehouse))
    for i, (dx, dy) in enumerate(moves):
        #print_warehouse(warehouse, robot, i, dx, dy)
        if i == 5:
            a = 3
        x, y = robot
        assert 0 <= x < dimensions[0] and 0 <= y < dimensions[1]
        nx, ny = x + dx, y + dy
        match warehouse[ny][nx]:
            case Tile.WALL:
                # do nothing
                pass
            case Tile.EMPTY:
                robot = (nx, ny)
            case Tile.BOX:
                raise Exception('impossible')

            case Tile.BOX_L | Tile.BOX_R if dy == 0:
                while warehouse[ny][nx] in [Tile.BOX_L, Tile.BOX_R]:
                    nx += dx
                    ny += dy

                match warehouse[ny][nx]:
                    case Tile.WALL:
                        # do nothing
                        pass
                    case Tile.EMPTY:
                        # shift Boxes
                        for i_x in range(nx, x, -dx):
                            warehouse[ny][i_x] = warehouse[y][i_x - dx]
                        robot = (x + dx, y + dy)
                    case _:
                        raise Exception('impossible')

            case Tile.BOX_L | Tile.BOX_R if dx == 0:
                if is_movable(warehouse, x, y, dy):
                    move_boxes(warehouse, x, y, dy)
                    robot = (x + dx, y + dy)
                else:
                    # do nothing
                    pass

            case _:
                raise Exception('impossible')
    #print_warehouse(warehouse, robot)
    score = 0
    for y, line in enumerate(warehouse):
        for x, t in enumerate(line):
            if t == Tile.BOX_L:
                score += 100 * y + x
    print('part2:', score)


def main(test: bool):
    warehouse, robot, moves = get_input(test)
    warehouse2 = []
    for line in warehouse:
        warehouse2.append([])
        for t in line:
            match t:
                case Tile.BOX:
                    warehouse2[-1].extend([Tile.BOX_L, Tile.BOX_R])
                case Tile.EMPTY | Tile.WALL:
                    warehouse2[-1].extend([t, t])
    part1(warehouse, robot, moves)
    part2(warehouse2, (robot[0] * 2, robot[1]), moves)


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
