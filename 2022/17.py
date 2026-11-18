from __future__ import annotations
import time

B_MINUS = [
    '@@@@',
]
B_PLUS = [
    '.@.',
    '@@@',
    '.@.',
]

B_L = [
    '..@',
    '..@',
    '@@@',
]
B_I = [
    '@',
    '@',
    '@',
    '@',
]
B_O = [
    '@@',
    '@@',
]


def get_input(test: bool) -> str:
    filename = 'inputs/17_test.txt' if test else 'inputs/17.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return input_[0].strip()


def insert_block(field: list[list[str]], block: list[str]) -> list[list[str]]:
    # pad block
    padded = []
    for row in block:
        padded.append(['.'] * 7)
        for i, c in enumerate(row, 2):
            padded[-1][i] = c
    for _ in range(3):
        padded.append(['.'] * 7)

    field = padded + field
    return field


def can_be_pushed(field: list[list[str]], dx: int, start: int, height_block: int) -> bool:
    for row in field[start:start + height_block]:
        # at wall?
        if (dx == -1 and row[0] == '@') or (dx == 1 and row[-1] == '@'):
            return False
        # nest to block
        if dx == -1:
            i = row.index('@')
        else:
            i = 50  # will throw out of bound error
            for j in range(len(row) - 1, -1, -1):
                if row[j] == '@':
                    i = j
                    break
        if row[i + dx] == '#':
            return False
    return True


def push_horizontal(
        field: list[list[str]],
        dx: int,
        start: int,
        height_block: int
) -> list[list[str]]:
    if can_be_pushed(field, dx, start, height_block):
        # push
        if dx == 1:
            iterator = range(5, -1, -1)
        else:
            iterator = range(1, 7)
        for row in field[start:start + height_block]:
            for i in iterator:
                if row[i] == '@':
                    row[i + dx] = '@'
                    row[i] = '.'

    return field


def can_fall(field: list[list[str]], start: int, height_block: int) -> bool:
    for y in range(start, start + height_block):
        for x, c in enumerate(field[y]):
            if c == '@':
                if y == len(field) - 1:
                    # bottom
                    return False
                if field[y + 1][x] == '#':
                    return False
    return True


def fall(field: list[list[str]], start: int, height_block: int) -> tuple[list[list[str]], bool]:
    if not can_fall(field, start, height_block):
        return field, False
    # fall
    for y in range(start + height_block - 1, start - 1, -1):
        for x, c in enumerate(field[y]):
            if c == '@':
                field[y + 1][x] = '@'
                field[y][x] = '.'
    return field, True


def main(test: bool, n_rocks: int) -> int:
    data = get_input(test)
    blocks = [B_MINUS, B_PLUS, B_L, B_I, B_O]
    field: list[list[str]] = []
    deleted_rows = 0
    rock_idx = 0        # rocks that have settled
    jet_idx = 0         # jets consumed so far
    seen: dict[tuple, tuple[int, int]] = {}

    # Top rows of the stack that fully determine the future.  The shapes are
    # at most 4 tall, so a few dozen rows is more than enough.
    H = 50

    while rock_idx < n_rocks:
        block = blocks[rock_idx % len(blocks)]
        height_block = len(block)
        field = insert_block(field, block)
        start = 0

        while True:
            jet = data[jet_idx % len(data)]
            jet_idx += 1
            field = push_horizontal(field, 1 if jet == '>' else -1, start, height_block)
            field, pushed = fall(field, start, height_block)

            if not pushed:
                # freeze block
                for row in field[start:start + height_block]:
                    for i in range(7):
                        if row[i] == '@':
                            row[i] = '#'
                # optimization: if there is a full line, cut off everything below
                for i, row in enumerate(field[start:start + height_block], start):
                    if row == ['#'] * 7:
                        deleted_rows += len(field) - i
                        field = field[:i]
                        break
                break

            # delete first row
            if field[0] == ['.'] * 7:
                field.pop(0)
            else:
                start += 1

        rock_idx += 1
        height = len(field) + deleted_rows

        # --- cycle detection -------------------------------------------------
        # The future depends only on: next rock, next jet, and the top of the
        # stack.  If we have seen this exact state before, the rocks in between
        # form a cycle that we can fast-forward over.
        signature = (
            rock_idx % len(blocks),
            jet_idx % len(data),
            tuple(''.join(row) for row in field[:H]),
        )
        if signature in seen:
            prev_rock, prev_height = seen[signature]
            cycle_rocks = rock_idx - prev_rock
            cycle_height = height - prev_height
            remaining = n_rocks - rock_idx
            if remaining >= cycle_rocks:
                cycles = remaining // cycle_rocks
                rock_idx += cycles * cycle_rocks
                deleted_rows += cycles * cycle_height
                seen.clear()
                continue
        seen[signature] = (rock_idx, height)

    return len(field) + deleted_rows


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    print('part 1:', main(True, 2022))
    print('part 2:', main(True, 1_000_000_000_000))

    print('real')
    print('part 1:', main(False, 2022))
    print('part 2:', main(False, 1_000_000_000_000))

    executionTime = (time.time() - startTime)
    if executionTime > 10:
        print(f'Execution time: {round(executionTime, 3)} s')

    else:
        print(f'Execution time: {round(executionTime * 1000, 3)} ms')
