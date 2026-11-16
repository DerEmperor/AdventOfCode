#!/usr/bin/env python
import os
import sys
import time
from heapq import heappush, heappop

original_stdout = sys.stdout

ENERGY_FACTOR = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

HOME_IDX_ROOM = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}

HOME_IDX_HALLWAY = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> str:
    data = []
    filename = 'inputs/23_test.txt' if test else 'inputs/23.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    rooms = (
            data[2][3] + data[3][3] + data[2][5] + data[3][5] +
            data[2][7] + data[3][7] + data[2][9] + data[3][9]
    )

    return rooms


def replace(old: str, idx: int, repl: str) -> str:
    return old[:idx] + repl + old[idx + 1:]


def part1(rooms: str) -> int:
    hallway = '.' * 11
    energy = 0
    queue = [(energy, hallway, rooms)]  # energy needs to be first for heapq
    best = {(hallway, rooms): 0}
    while queue:
        energy, hallway, rooms = heappop(queue)
        print('\r', energy, end='', flush=True)
        if rooms == 'AABBCCDD':
            print('\r          ')
            return energy
        if energy > best.get((hallway, rooms), float('inf')):
            # stale queue entry, a cheaper path to this state already exists
            continue
        # get moves
        # 1. move out of rooms
        rooms_split = [rooms[:2], rooms[2:4], rooms[4:6], rooms[6:8]]
        for i, room in zip([2, 4, 6, 8], rooms_split):
            if room == '..':
                continue
            if room[0] == room[1] and i == HOME_IDX_HALLWAY[room[1]]:
                # don't leave home
                continue
            if room[0] == '.':
                base_moves = 2
                letter = room[1]
            else:
                base_moves = 1
                letter = room[0]
            # entrance is never blocked
            # move left
            for next_i in range(i - 1, -1, -1):
                if hallway[next_i] != '.':
                    # occupied
                    break
                if next_i in HOME_IDX_HALLWAY.values():
                    # amphipods never stop right outside a room, but may pass through
                    continue
                new_hallway = replace(hallway, next_i, letter)
                new_rooms = replace(rooms, i + base_moves - 3, '.')
                new_energy = energy + (base_moves + i - next_i) * ENERGY_FACTOR[letter]
                if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                    best[(new_hallway, new_rooms)] = new_energy
                    heappush(queue, (new_energy, new_hallway, new_rooms))
            # move right
            for next_i in range(i + 1, 11):
                if hallway[next_i] != '.':
                    # occupied
                    break
                if next_i in HOME_IDX_HALLWAY.values():
                    # amphipods never stop right outside a room, but may pass through
                    continue
                new_hallway = replace(hallway, next_i, letter)
                new_rooms = replace(rooms, i + base_moves - 3, '.')
                new_energy = energy + (base_moves + next_i - i) * ENERGY_FACTOR[letter]
                if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                    best[(new_hallway, new_rooms)] = new_energy
                    heappush(queue, (new_energy, new_hallway, new_rooms))
        # hallway -> room
        for i, letter in enumerate(hallway):
            if hallway[i] == '.':
                continue
            # is room ready?
            room = rooms_split[HOME_IDX_ROOM[letter]]
            if room[0] != '.':
                # full
                continue
            if room[1] not in ['.', letter]:
                # other letter in room
                continue
            home_idx_hallway = HOME_IDX_HALLWAY[letter]
            step = 1 if home_idx_hallway < i else -1
            if any(c != '.' for c in hallway[home_idx_hallway:i:step]):
                # path is blocked
                continue
            # make move
            room_idx = 1 if room[1] == '.' else 0
            new_hallway = replace(hallway, i, '.')
            new_rooms = replace(rooms, 2 * HOME_IDX_ROOM[letter] + room_idx, letter)
            new_energy = energy + (abs(i - home_idx_hallway) + room_idx + 1) * ENERGY_FACTOR[letter]
            if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                best[(new_hallway, new_rooms)] = new_energy
                heappush(queue, (new_energy, new_hallway, new_rooms))
    print('\r          ')
    return -1


def part2(rooms: str) -> int:
    hallway = '.' * 11
    energy = 0
    queue = [(energy, hallway, rooms)]  # energy needs to be first for heapq
    best = {(hallway, rooms): 0}
    while queue:
        energy, hallway, rooms = heappop(queue)
        print('\r', energy, end='', flush=True)
        if rooms == 'AAAABBBBCCCCDDDD':
            print('\r          ')
            return energy
        if energy > best.get((hallway, rooms), float('inf')):
            # stale queue entry, a cheaper path to this state already exists
            continue
        # get moves
        # 1. move out of rooms
        rooms_split = [rooms[:4], rooms[4:8], rooms[8:12], rooms[12:16]]
        for i, room in zip([2, 4, 6, 8], rooms_split):
            if room == '....':
                continue
            if room[0] == room[1] == room[2] == room[3] and i == HOME_IDX_HALLWAY[room[3]]:
                # don't leave home
                continue
            if room[0] != '.':
                base_moves = 1
                letter = room[0]
            elif room[1] != '.':
                base_moves = 2
                letter = room[1]
            elif room[2] != '.':
                base_moves = 3
                letter = room[2]
            else:
                base_moves = 4
                letter = room[3]
            # entrance is never blocked
            # move left
            for next_i in range(i - 1, -1, -1):
                if hallway[next_i] != '.':
                    # occupied
                    break
                if next_i in HOME_IDX_HALLWAY.values():
                    # amphipods never stop right outside a room, but may pass through
                    continue
                new_hallway = replace(hallway, next_i, letter)
                new_rooms = replace(rooms, 4 * ((i - 2) // 2) + base_moves - 1, '.')
                new_energy = energy + (base_moves + i - next_i) * ENERGY_FACTOR[letter]
                if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                    best[(new_hallway, new_rooms)] = new_energy
                    heappush(queue, (new_energy, new_hallway, new_rooms))
            # move right
            for next_i in range(i + 1, 11):
                if hallway[next_i] != '.':
                    # occupied
                    break
                if next_i in HOME_IDX_HALLWAY.values():
                    # amphipods never stop right outside a room, but may pass through
                    continue
                new_hallway = replace(hallway, next_i, letter)
                new_rooms = replace(rooms, 4 * ((i - 2) // 2) + base_moves - 1, '.')
                new_energy = energy + (base_moves + next_i - i) * ENERGY_FACTOR[letter]
                if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                    best[(new_hallway, new_rooms)] = new_energy
                    heappush(queue, (new_energy, new_hallway, new_rooms))
        # hallway -> room
        for i, letter in enumerate(hallway):
            if hallway[i] == '.':
                continue
            # is room ready?
            room = rooms_split[HOME_IDX_ROOM[letter]]
            if room[0] != '.':
                # full
                continue
            if room[1] not in ['.', letter]:
                # other letter in room
                continue
            if room[2] not in ['.', letter]:
                # other letter in room
                continue
            if room[3] not in ['.', letter]:
                # other letter in room
                continue
            home_idx_hallway = HOME_IDX_HALLWAY[letter]
            step = 1 if home_idx_hallway < i else -1
            if any(c != '.' for c in hallway[home_idx_hallway:i:step]):
                # path is blocked
                continue
            # make move
            if room[3] == '.':
                room_idx = 3
            elif room[2] == '.':
                room_idx = 2
            elif room[1] == '.':
                room_idx = 1
            else:
                room_idx = 0
            new_hallway = replace(hallway, i, '.')
            new_rooms = replace(rooms, 4 * HOME_IDX_ROOM[letter] + room_idx, letter)
            new_energy = energy + (abs(i - home_idx_hallway) + room_idx + 1) * ENERGY_FACTOR[letter]
            if new_energy < best.get((new_hallway, new_rooms), float('inf')):
                best[(new_hallway, new_rooms)] = new_energy
                heappush(queue, (new_energy, new_hallway, new_rooms))
    print('\r          ')
    return -1


def main(test: bool):
    rooms = get_input(test)

    sum1 = part1(rooms)
    rooms = (
        f'{rooms[0]}DD{rooms[1]}'
        f'{rooms[2]}CB{rooms[3]}'
        f'{rooms[4]}BA{rooms[5]}'
        f'{rooms[6]}AC{rooms[7]}'
    )
    sum2 = part2(rooms)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [12521, 18195]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [44169, 50265]:
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
