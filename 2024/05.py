#!/usr/bin/env python
import time
from collections import defaultdict


def get_input(test):
    filename = 'inputs/05_test.txt' if test else 'inputs/05.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    input_iter = iter(input_)

    rules = defaultdict(list)
    for line in input_iter:
        if line == '\n':
            break
        a, b = [int(x) for x in line[:-1].split('|')]
        rules[a].append(b)

    pages = []
    for line in input_iter:
        pages.append([int(x) for x in line[:-1].split(',')])
    return rules, pages


def main(test):
    rules, pagess = get_input(test)

    part1 = 0
    part2 = 0

    for pages in pagess:
        valid = True
        for i, page_a in enumerate(pages):
            for page_b in pages[i + 1:]:
                if page_b not in rules[page_a]:
                    valid = False
                    break
            if not valid:
                break

        if valid:
            part1 += pages[len(pages) // 2]

        else:
            corrected_pages = [pages[0]]
            for page_ins in pages[1:]:
                for i, page_b in enumerate(corrected_pages):
                    if page_ins not in rules[page_b]:
                        corrected_pages.insert(i, page_ins)
                        break
                if page_ins not in corrected_pages:
                    corrected_pages.append(page_ins)
            part2 += corrected_pages[len(corrected_pages) // 2]

    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
