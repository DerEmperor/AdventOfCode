import time
import re


def get_input(test):
    filename = 'inputs/05_test.txt' if test else 'inputs/05.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    index = re.compile(r'( \d+ {2})+')
    instruction = re.compile(r'move (\d+) from (\d+) to (\d+)\n')

    instructions = []

    number_stacks = len(input_[0]) // 3 - 1
    crates = [[] for _ in range(number_stacks)]

    i = 0
    for i, line in enumerate(input_):
        if index.match(line):
            break
        for j, crate in enumerate(line[1::4]):
            if crate != ' ':
                crates[j].insert(0, crate)

    for line in input_[i + 2:]:
        match = instruction.match(line)
        assert match
        instructions.append(tuple(map(int, match.groups())))

    return crates, instructions


def main(test):
    crates, instructions = get_input(test)

    # part 1
    crates1 = [stack[:] for stack in crates]
    for num, src, dst in instructions:
        for _ in range(num):
            crates1[dst-1].append(crates1[src-1].pop())

    message = ''
    for stack in crates1:
        if stack:
            message = message + stack[-1]
    print('part 1:', message)

    # part 2
    crates2 = [stack[:] for stack in crates]
    for num, src, dst in instructions:
        tmp = []
        for _ in range(num):
            tmp.insert(0, crates2[src-1].pop())
        crates2[dst-1].extend(tmp)

    message = ''
    for stack in crates2:
        if stack:
            message = message + stack[-1]
    print('part 2:', message)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
