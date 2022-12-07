from __future__ import annotations
from typing import *
import time

TOTAL_SPACE = 70000000
NEEDED_SPACE = 30000000
THRESHOLD_PART1 = 100000


class CodeUnreachable(Exception):
    pass


class Dir:
    def __init__(self, name: str):
        self.name = name
        self._sub_dirs: List[Dir] = []
        self._files: List[File] = []
        self.parent = None

    @property
    def size(self):
        res = 0
        for dir in self._sub_dirs:
            res += dir.size
        for file in self._files:
            res += file.size
        return res

    def add_dir(self, dir: Dir):
        self._sub_dirs.append(dir)
        dir.parent = self

    def add_file(self, file: File):
        self._files.append(file)

    def sub_dirs(self):
        for dir in self._sub_dirs:
            yield dir

    def files(self):
        for file in self._files:
            yield file

    def get_sub_dir_by_name(self, name: str):
        for dir in self._sub_dirs:
            if dir.name == name:
                return dir
        return None


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


def get_input(test: bool) -> List[str]:
    filename = 'inputs/07_test.txt' if test else 'inputs/07.txt'
    with open(filename, 'r') as file:
        input_ = file.read()
    return input_.split('\n')[:-1]


def get_score1(cwd: Dir) -> int:
    res = 0
    for dir in cwd.sub_dirs():
        if dir.size <= THRESHOLD_PART1:
            res += dir.size
        res += get_score1(dir)
    return res


def get_score2(cwd: Dir, current_solution: int, needed_space: int) -> int:
    for dir in cwd.sub_dirs():
        if needed_space <= dir.size < current_solution:
            current_solution = dir.size

        current_solution = get_score2(dir, current_solution, needed_space)

    return current_solution


def main(test: bool):
    data = get_input(test)
    tree = Dir('/')
    cwd = tree

    i = 0
    # build tree
    while i < len(data):
        command = data[i][2:]  # cut of '$ '
        if command == 'cd ..':
            cwd = cwd.parent
            i += 1
        elif command == 'cd /':
            cwd = tree
            i += 1
        elif command.startswith('cd '):
            dst = command[3:]
            cwd = cwd.get_sub_dir_by_name(dst)
            i += 1
        elif command == 'ls':
            i += 1
            while i < len(data) and data[i][0] != '$':
                line = data[i]
                if line.startswith('dir '):
                    dir_name = line[4:]
                    cwd.add_dir(Dir(dir_name))
                else:
                    size, name = line.split(' ')
                    cwd.add_file(File(name, int(size)))
                i += 1

        else:
            raise CodeUnreachable

    print(get_score1(tree))
    print(get_score2(tree, tree.size, NEEDED_SPACE - (TOTAL_SPACE - tree.size)))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
