import time
import re
import numpy as np


def get_input(test):
    filename = 'inputs/10_test.txt' if test else 'inputs/10.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    # input_ = ['noop\n', 'addx 3\n', 'addx -5\n']
    program = []
    for line in input_:
        if line == 'noop\n':
            program.append(None)
        else:
            assert line.startswith('addx ')
            program.append(int(line[5:-1]))
    return program


def main(test):
    program = get_input(test)
    x = 1
    cycle = 0
    instruction_counter = 0
    score = 0
    wait = False
    screen = ''
    while instruction_counter < len(program):
        cycle += 1
        # eval here
        if cycle in range(20, 230, 40):
            score += cycle * x

        if (cycle - 1) % 40 == 0 and cycle != 1:
            screen = screen + '\n'
        screen = screen + ('#' if abs((cycle - 1) % 40 - x) <= 1 else '.')

        # do stuff
        val = program[instruction_counter]
        if val is None:
            instruction_counter += 1
        else:
            if wait:
                x += val
                wait = False
                instruction_counter += 1
            else:
                wait = True
    cycle += 1
    print(score)
    print(screen)
    print()


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
