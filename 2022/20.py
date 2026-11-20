#!/usr/bin/env python
import os
import sys
import time
from operator import contains

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


class Node:
    cnt = 0

    def __init__(self, val: int, prev: Node | None):
        self.val = val
        self.next = None
        self.prev = prev
        self.id = Node.cnt
        Node.cnt += 1

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __str__(self):
        return f'<Node {self.id}>'

    def __repr__(self):
        return f'<Node {self.id}, {repr(self.val)}, {str(self.next)}, {str(self.prev)}>'


def get_input(test: bool) -> list[int]:
    data = []
    filename = 'inputs/20_test.txt' if test else 'inputs/20.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(int(line[:-1]))
    return data


def build_list(data: list[int]) -> Node:
    Node.cnt = 0
    first = Node(data[0], None)
    prev = first
    for val in data[1:]:
        node = Node(val, prev)
        prev.next = node
        prev = node
    node.next = first
    first.prev = node
    return first


def list_to_array(head: Node) -> list[int]:
    cur = head
    result = []
    while cur.next != head:
        result.append(cur.val)
        cur = cur.next
    result.append(head.prev.val)
    return result


def mix(length: int, positions: dict[int, Node]):
    for cnt in range(length):
        cur = positions[cnt]

        # while cur is detached the circle has length - 1 nodes, so moving
        # by cur.val is equivalent to moving forward by cur.val % (length - 1)
        # (Python's % already maps negative values to the forward equivalent).
        # A result of 0 means cur lands back in its own gap: no movement.
        hops = cur.val % (length - 1)
        if hops == 0:
            continue

        pnt = cur

        # remove cur
        cur.prev.next = cur.next
        cur.next.prev = cur.prev

        # move pnt
        # forward `hops` hops and going m - hops net steps backward land at
        # the same position, but the first backward hop from the detached
        # node only reaches the gap, so the backward walk needs one hop
        # more: m + 1 - hops with m = length - 1. Walk whichever is shorter.
        m = length - 1
        if hops * 2 <= m + 1:
            for _ in range(hops):
                pnt = pnt.next
        else:
            for _ in range(m + 1 - hops):
                pnt = pnt.prev

        # insert cur after pnt
        cur.next = pnt.next
        cur.prev = pnt
        pnt.next = cur
        cur.next.prev = cur


def get_coords(head: Node) -> int:
    cur = head
    while cur.val != 0:
        cur = cur.next
    coords = []
    for _ in range(3):
        for _ in range(1000):
            cur = cur.next
        coords.append(cur.val)
    return sum(coords)


def solve(head: Node, length: int, rounds: int) -> int:
    # remember positions
    cur = head
    positions: dict[int, Node] = {}
    while cur.next != head:
        positions[cur.id] = cur
        cur = cur.next
    positions[cur.id] = cur

    for _ in range(rounds):
        mix(length, positions)
    return get_coords(head)


def main(test: bool):
    data_array = get_input(test)
    head = build_list(data_array)
    sum1 = solve(head, len(data_array), 1)

    data_array = [x * 811589153 for x in data_array]
    head = build_list(data_array)
    sum2 = solve(head, len(data_array), 10)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [3, 4151]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [1623178306, 7848878698663]:
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
