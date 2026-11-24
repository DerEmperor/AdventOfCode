#!/usr/bin/env python
import os
import random
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> tuple[dict[str, int], dict[str, tuple[str, str, str]]]:
    inputs = {}
    instructions = {}
    filename = 'inputs/24_test3.txt' if test else 'inputs/24.txt'
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                break
            a, b = line.strip().split(': ')
            inputs[a] = int(b)
        for line in file:
            instr, dst = line.strip().split(' -> ')
            instructions[dst] = tuple(instr.split(' '))
    return inputs, instructions


def trace(data: dict[str, int | tuple[str, str, str]], wire: str) -> int:
    if isinstance(data[wire], int):
        return data[wire]

    a, op, b = data[wire]
    a = trace(data, a)
    b = trace(data, b)
    match op:
        case 'AND':
            res = a & b
        case 'OR':
            res = a | b
        case 'XOR':
            res = a ^ b
        case _:
            assert False
    data[wire] = res
    return res


def part1(data: dict[str, int | tuple[str, str, str]]) -> int:
    res = ''
    for i in range(64):
        wire = f'z{i:02d}'
        if wire not in data:
            break
        tmp = trace(data, wire)
        assert tmp in [0, 1]
        res = str(tmp) + res
    return int(res, 2)


def part2(data: dict[str, int | tuple[str, str, str]]) -> str:
    # the outputs of a few pairs of gates were swapped; find the affected wires
    n = 0
    while f'z{n:02d}' in data:
        n += 1
    gates = {k: v for k, v in data.items() if isinstance(v, tuple)}
    x_names = sorted(k for k in data if k[0] == 'x' and isinstance(data[k], int))
    y_names = sorted(k for k in data if k[0] == 'y' and isinstance(data[k], int))
    rng = random.Random(42)

    def run(xv, yv):
        d = {**gates, **xv, **yv}
        res = 0
        for i in reversed(range(n)):
            res = (res << 1) | trace(d, f'z{i:02d}')
        return res

    def rand():
        return ({x: rng.randint(0, 1) for x in x_names},
                {y: rng.randint(0, 1) for y in y_names})

    def xy_pair(a, b):
        return {a[0], b[0]} == {'x', 'y'} and a[1:] == b[1:]

    if all(xy_pair(a, b) and w[0] == 'z' for w, (a, op, b) in gates.items()):
        # flat circuit: every gate reads an x/y pair, so it belongs to the z wire
        # of the same bit (24_test3.txt)
        suspects = set()
        ops = {}
        for i in range(n):
            for w, (a, op, b) in gates.items():
                if {a, b} == {f'x{i:02d}', f'y{i:02d}'}:
                    ops[i] = op
                    if w != f'z{i:02d}':
                        suspects.update((f'z{i:02d}', w))
                        gates[f'z{i:02d}'], gates[w] = gates[w], gates[f'z{i:02d}']
                    break
        # after undoing the swaps every gate drives its own bit again
        for _ in range(20):
            xv, yv = rand()
            z = run(xv, yv)
            for i, op in ops.items():
                match op:
                    case 'AND':
                        expected = xv[f'x{i:02d}'] & yv[f'y{i:02d}']
                    case 'OR':
                        expected = xv[f'x{i:02d}'] | yv[f'y{i:02d}']
                    case _:
                        expected = xv[f'x{i:02d}'] ^ yv[f'y{i:02d}']
                assert ((z >> i) & 1) == expected
        return ','.join(sorted(suspects))

    # the real circuit is a ripple-carry adder that should compute x + y
    def failing(xv, yv):
        # the bits where the circuit disagrees with x + y
        x = sum(b << int(k[1:]) for k, b in xv.items())
        y = sum(b << int(k[1:]) for k, b in yv.items())
        z = run(xv, yv)
        expect = x + y
        return {i for i in range(n) if ((z >> i) & 1) != ((expect >> i) & 1)}

    ones_x = {x: 1 for x in x_names}
    ones_y = {y: 1 for y in y_names}
    zero_x = {x: 0 for x in x_names}
    zero_y = {y: 0 for y in y_names}
    # carry-maximizing inputs expose every carry wire and z gate at once
    battery = [
        (ones_x, ones_y),
        ({**zero_x, x_names[0]: 1}, ones_y),
        (ones_x, {**zero_y, y_names[0]: 1}),
        (ones_x, zero_y),
        (zero_x, ones_y),
    ] + [rand() for _ in range(5)]

    def all_failing():
        s = set()
        for xv, yv in battery:
            s |= failing(xv, yv)
        return s

    # every z wire is driven by an XOR of two gate outputs (the top one by the carry OR)
    def wrong_z_gate(i):
        a, op, b = gates[f'z{i:02d}']
        if i == 0:
            return not (op == 'XOR' and xy_pair(a, b))
        if i == n - 1:
            return op != 'OR'
        return not (op == 'XOR' and not xy_pair(a, b))

    flagged = [f'z{i:02d}' for i in range(n) if wrong_z_gate(i)]
    # displaced z gates: XORs of two gate outputs that drive an ordinary wire
    displaced = [w for w, (a, op, b) in gates.items()
                 if w[0] != 'z' and op == 'XOR' and not xy_pair(a, b)]

    # pair every wrong z gate with the displaced gate of the same bit:
    # both read the same half-sum wire
    gate_of = {}
    for w, (a, op, b) in gates.items():
        gate_of.setdefault((op, frozenset((a, b))), w)
    swapped = set()
    for z in flagged:
        i = int(z[1:])
        h = gate_of.get(('XOR', frozenset((f'x{i:02d}', f'y{i:02d}'))))
        if h is None:
            continue  # no half-sum gate: not an adder
        for w in displaced:
            if w in swapped:
                continue
            a, _, b = gates[w]
            if h in (a, b):
                swapped.update((z, w))
                gates[z], gates[w] = gates[w], gates[z]
                break

    # which wires each wire can influence: a repairing pair has to reach every
    # broken bit, so this prunes the search
    consumers = {}
    for w, (a, op, b) in gates.items():
        for inp in (a, b):
            consumers.setdefault(inp, []).append(w)

    fanout_cache = {}

    def fanout(w):
        if w not in fanout_cache:
            seen = set()
            todo = [w]
            while todo:
                t = todo.pop()
                if t in seen:
                    continue
                seen.add(t)
                todo.extend(consumers.get(t, ()))
            fanout_cache[w] = seen
        return fanout_cache[w]

    while all_failing():
        target = {f'z{i:02d}' for i in all_failing()}
        found = False
        for u in sorted(gates):
            for v in sorted(gates):
                if v <= u:
                    continue
                # the pair has to reach every broken bit, or it can not repair them
                if not target <= fanout(u) | fanout(v):
                    continue
                gates[u], gates[v] = gates[v], gates[u]
                try:
                    if not all_failing():
                        swapped.update((u, v))
                        found = True
                        break
                except RecursionError:
                    pass  # the swap created a cycle: not a valid pair
                gates[u], gates[v] = gates[v], gates[u]
            if found:
                break
        if not found:
            return ''  # nothing repairs the circuit: not a broken adder

    # the repaired circuit must add correctly on arbitrary inputs
    for _ in range(200):
        xv, yv = rand()
        assert not failing(xv, yv), 'the repair does not add correctly'
    return ','.join(sorted(swapped))


def main(test: bool):
    inputs, instructions = get_input(test)

    sum1 = part1({**inputs, **instructions})
    sum2 = part2({**inputs, **instructions})

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [4, 2024, 9, 55920211035878]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in ['z00,z01,z02,z05', 'btb,cmv,mwp,rdg,rmj,z17,z23,z30']:
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
