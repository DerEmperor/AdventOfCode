import time
import re
import numpy as np
import inspect
from math import lcm

part1 = False


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level

    def apply_operation(self, operation, mod=1):
        self.worry_level = operation(self.worry_level)
        if part1:
            self.worry_level = self.worry_level // 3
        else:
            self.worry_level = self.worry_level % mod

    def __repr__(self):
        return f'<Item {self.worry_level}>'


class Monkey:
    lcm = 0
    def __init__(self, id, items, operation, divisible_test, on_true, on_false):
        self.id = id
        self.items = items
        self.operation = operation
        self.divisible_test = divisible_test
        self.on_true = on_true
        self.on_false = on_false
        self.inspection_counter = 0

    def has_items(self):
        return len(self.items) != 0

    def throw(self):
        item = self.items.pop(0)
        item.apply_operation(self.operation, self.lcm)
        self.inspection_counter += 1
        if item.worry_level % self.divisible_test == 0:
            return self.on_true, item
        else:
            return self.on_false, item

    def __repr__(self):
        return f'Monkey {self.id}: {self.items}'


def get_input(test):
    filename = 'inputs/11_test.txt' if test else 'inputs/11.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    input_.append('\n')
    monkeys = dict()

    for i in range(0, len(input_), 7):
        id = i // 7
        assert input_[i] == f'Monkey {id}:\n'
        assert input_[i + 1].startswith('  Starting items: ')
        assert input_[i + 2].startswith('  Operation: new =')
        assert input_[i + 3].startswith('  Test: divisible by ')
        assert input_[i + 4].startswith('    If true: throw to monkey ')
        assert input_[i + 5].startswith('    If false: throw to monkey ')
        assert input_[i + 6] == '\n'

        monkey = Monkey(
            id=id,
            items=[Item(int(x)) for x in input_[i + 1][len('  Starting items: '):-1].split(', ')],
            operation=eval('lambda old: ' + input_[i + 2][len('  Operation: new = '):-1]),
            divisible_test=int(input_[i + 3][len('  Test: divisible by '):-1]),
            on_true=int(input_[i + 4][len('    If true: throw to monkey '):-1]),
            on_false=int(input_[i + 5][len('    If false: throw to monkey '):-1]),
        )
        monkeys[id] = monkey

    Monkey.lcm = lcm(*[m.divisible_test for m in monkeys.values()])

    return monkeys


def main(test):
    monkeys = get_input(test)
    rounds = 20 if part1 else 10000
    for round in range(rounds):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            while monkey.has_items():
                dst, item = monkey.throw()
                monkeys[dst].items.append(item)

    # score 1
    inspections = sorted([m.inspection_counter for m in monkeys.values()], reverse=True)
    print(inspections[0] * inspections[1])


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
