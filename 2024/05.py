#!/usr/bin/env python
import time
from collections import defaultdict


class Page:
    rules = {}

    def __init__(self, page):
        self.page = page

    def __lt__(self, other):
        return other.page in Page.rules[self.page]

    def __eq__(self, other):
        return self.page == other.page

    def __str__(self):
        return str(self.page)

    def __repr__(self):
        return f'A({self.page})'


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
    pagess = [[Page(page) for page in pages] for pages in pagess]
    Page.rules = rules

    part1 = 0
    part2 = 0

    for pages in pagess:
        pages_sorted = sorted(pages)
        if pages == pages_sorted:
            part1 += pages[len(pages) // 2].page
        else:
            part2 += pages_sorted[len(pages) // 2].page

    print('part1:', part1)
    print('part2:', part2)


def main2(test):
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
