#!/usr/bin/env python
import time

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_input(test: bool):
    data = []
    filename = 'inputs/18_test.txt' if test else 'inputs/18.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(tuple(int(x) for x in line[:-1].split(',')))
    dimensions = (7, 7) if test else (71, 71)
    return data, dimensions


def print_maze(walls, dimensions):
    grid = [['.' for _ in range(dimensions[0])] for _ in range(dimensions[1])]
    for x, y in walls:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))
    print()


def main(test: bool):
    data, dimensions = get_input(test)
    end = 12 if test else 1024
    goal = (dimensions[0] - 1, dimensions[1] - 1)
    possible = True

    while possible:
        walls = set(data[:end])
        todo = [((0, 0), 0)]  # (x, y), steps
        visited = {(0, 0)}
        possible = False
        while todo:
            pos, steps = todo.pop(0)
            if pos == goal:
                if end == (12 if test else 1024):
                    print('part1:', steps)
                possible = True
                break
            x, y = pos
            for dx, dy in DIRECTIONS:
                new_pos = (x + dx, y + dy)
                if (
                        0 <= x + dx < dimensions[0] and 0 <= y + dy < dimensions[1] and
                        new_pos not in visited and
                        new_pos not in walls
                ):
                    todo.append((new_pos, steps + 1))
                    visited.add(new_pos)
        end += 1
        #print_maze(walls, dimensions)
    print('part2: ', data[end-2][0], ',', data[end-2][1], sep='')


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
