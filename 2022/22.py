#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> tuple[list[str], str]:
    field = []
    filename = 'inputs/22_test.txt' if test else 'inputs/22.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            field.append(line[:-1])
    instructions = field[-1]
    field = field[:-2]
    return field, instructions


class InstructionsIter:
    def __init__(self, instructions: str):
        self.instructions = instructions

    def __iter__(self):
        self.cnt = 0
        return self

    def __next__(self) -> int | str:
        try:
            if self.instructions[self.cnt] not in 'RL':
                number = ''
                while self.cnt < len(self.instructions) and self.instructions[self.cnt] not in 'RL':
                    number += self.instructions[self.cnt]
                    self.cnt += 1
                return int(number)
            else:
                res = self.instructions[self.cnt]
                self.cnt += 1
                return res
        except IndexError:
            raise StopIteration


TURN_LEFT = {
    (0, 1): (1, 0),
    (0, -1): (-1, 0),
    (1, 0): (0, -1),
    (-1, 0): (0, 1),
}

TURN_RIGHT = {
    (0, 1): (-1, 0),
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
}

DIR_SCORE = {
    (0, 1): 1,
    (0, -1): 3,
    (-1, 0): 2,
    (1, 0): 0,
}


def vadd(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vmul(k: int, a: tuple[int, int, int]) -> tuple[int, int, int]:
    return (k * a[0], k * a[1], k * a[2])


def vcross(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def fold_cube(field: list[str]) -> tuple[int, dict, dict]:
    """Fold the map (a net of six N×N faces) into a cube in 3D.

    Returns (N, placement, edges):
    - N: side length of the faces
    - placement: face tile (top-left map position) -> (P, u, v), where P is
      the 3D corner of the face's top-left cell, u the 3D direction of
      increasing map row and v of increasing map column
    - edges: 3D midpoint of each surface edge -> the two (face, i, j) cells
      that share it

    All 3D coordinates are doubled so that cell centers (odd coordinates)
    and edge midpoints (even coordinates) stay integers.
    """
    height = len(field) - 2  # map rows, without padding
    width = len(field[1]) - 2  # map columns, without padding

    # the map consists of six N×N blocks on an N grid; find N
    N = 0
    faces = []
    for n in range(min(height, width), 0, -1):
        if height % n or width % n:
            continue
        blocks = []
        clean = True
        for r0 in range(1, height + 1, n):
            for c0 in range(1, width + 1, n):
                cells = [field[r][c] for r in range(r0, r0 + n) for c in range(c0, c0 + n)]
                if all(ch in '.#' for ch in cells):
                    blocks.append((r0, c0))
                elif any(ch in '.#' for ch in cells):
                    clean = False  # half-filled block: wrong n
        if clean and len(blocks) == 6:
            N = n
            faces = blocks
            break
    assert N, 'map is not a net of six square faces'

    # place the first face, then fold the others around the shared edges
    placement = {faces[0]: ((0, 0, 0), (1, 0, 0), (0, 1, 0))}
    queue = [faces[0]]
    while queue:
        face = queue.pop()
        P, u, v = placement[face]
        w = vcross(u, v)
        for dr0, dc0 in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbour = (face[0] + dr0 * N, face[1] + dc0 * N)
            if neighbour not in faces or neighbour in placement:
                continue
            if dr0 == -1:  # above: fold down over the top edge
                placement[neighbour] = (vadd(P, vmul(2 * N, w)), vmul(-1, w), v)
            elif dr0 == 1:  # below: fold up over the bottom edge
                placement[neighbour] = (vadd(P, vmul(2 * N, u)), w, v)
            elif dc0 == -1:  # left: fold over the left edge
                placement[neighbour] = (vadd(P, vmul(2 * N, w)), u, vmul(-1, w))
            else:  # right: fold over the right edge
                placement[neighbour] = (vadd(P, vmul(2 * N, v)), u, w)
            queue.append(neighbour)
    assert len(placement) == 6, 'net is not connected'

    # all cell centers and the midpoints of the edges between cells
    centres = {}
    edges = {}
    for face, (P, u, v) in placement.items():
        for i in range(N):
            for j in range(N):
                centre = vadd(vadd(P, vmul(2 * i + 1, u)), vmul(2 * j + 1, v))
                assert centre not in centres, 'faces overlap in 3D'
                centres[centre] = (face, i, j)
                for edge in (vadd(centre, u), vadd(centre, vmul(-1, u)),
                             vadd(centre, v), vadd(centre, vmul(-1, v))):
                    edges.setdefault(edge, []).append((face, i, j))
    # every edge is shared by exactly two cells: the cube is closed
    assert all(len(cells) == 2 for cells in edges.values()), 'net does not close into a cube'
    # the six faces lie on the six distinct sides of the cube
    assert len({vcross(u, v) for (_, u, v) in placement.values()}) == 6
    return N, placement, edges


def nextfield(field: list[str], x: int, y: int, dx: int, dy: int, cube: tuple | None) -> tuple[int, int, int, int]:
    """Attempt one step from (x, y) in direction (dx, dy).

    Returns the new position and the direction after the step; crossing an
    edge of the cube also changes the direction. cube is None for the flat
    wrap-around of part 1 or (N, placement, edges) from fold_cube() for
    part 2."""
    nx = x + dx
    ny = y + dy
    if field[ny][nx] != ' ':
        return nx, ny, dx, dy
    if cube is None:
        nx = x
        ny = y
        # wrap, go back
        while field[ny][nx] in '.#':
            nx -= dx
            ny -= dy
        nx += dx
        ny += dy
        return nx, ny, dx, dy

    # left the net: cross the edge onto the neighbouring cube face
    N, placement, edges = cube
    face = (1 + (y - 1) // N * N, 1 + (x - 1) // N * N)  # face tile of (x, y)
    i = (y - 1) % N
    j = (x - 1) % N
    P, u, v = placement[face]
    centre = vadd(vadd(P, vmul(2 * i + 1, u)), vmul(2 * j + 1, v))
    edge = vadd(centre, vadd(vmul(dy, u), vmul(dx, v)))  # crossed cube edge
    # the cell on the other side of the edge
    face2, i2, j2 = next(c for c in edges[edge] if c != (face, i, j))
    P2, u2, v2 = placement[face2]
    centre2 = vadd(vadd(P2, vmul(2 * i2 + 1, u2)), vmul(2 * j2 + 1, v2))
    # direction from the edge into the new cell, in the new face's axes
    into = vadd(centre2, vmul(-1, edge))
    if into == u2:
        ndy, ndx = 1, 0
    elif into == vmul(-1, u2):
        ndy, ndx = -1, 0
    elif into == v2:
        ndy, ndx = 0, 1
    else:
        assert into == vmul(-1, v2)
        ndy, ndx = 0, -1
    return face2[1] + j2, face2[0] + i2, ndx, ndy


def walk(field: list[str], instructions: str, cube: bool):
    cube_data = fold_cube(field) if cube else None
    inst_iter = InstructionsIter(instructions)
    y = 1
    x = field[1].index('.')
    dx = 1
    dy = 0
    for instruction in inst_iter:
        if instruction == 'L':
            dx, dy = TURN_LEFT[(dx, dy)]
            continue
        if instruction == 'R':
            dx, dy = TURN_RIGHT[(dx, dy)]
            continue

        # Walk
        for _ in range(instruction):
            nx, ny, ndx, ndy = nextfield(field, x, y, dx, dy, cube_data)
            if field[ny][nx] == '#':
                break
            x = nx
            y = ny
            dx = ndx
            dy = ndy

    return y * 1000 + x * 4 + DIR_SCORE[(dx, dy)]


def main(test: bool):
    field, instructions = get_input(test)

    # pad field
    length = max(len(line) for line in field) + 2
    for y in range(len(field)):
        line = field[y]
        field[y] = ' ' + line + (' ' * (length - len(line) - 1))
    field.insert(0, ' ' * length)
    field.append(' ' * length)

    sum1 = walk(field, instructions, False)
    sum2 = walk(field, instructions, True)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [6032, 191010]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [5031, 55364]:
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
