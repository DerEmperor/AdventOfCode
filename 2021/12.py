import time


def main():
    with open('12_input.txt', 'r') as file:
        input_ = file.readlines()

    connections = dict()
    for line in input_:
        a, b = line[:-1].split('-')
        if a not in connections:
            connections[a] = []
        if b not in connections:
            connections[b] = []
        if b != 'start':
            connections[a].append(b)
        if a != 'start':
            connections[b].append(a)

    paths_single = []
    paths_twice = []
    twice = ''
    path = []
    visited = set()

    get_pathes('start', connections, paths_single, paths_twice, path, visited, twice)

    print(len(paths_single))
    print(len(paths_twice))


def get_pathes(cave, connections, paths_single, paths_twice, path, visited, twice):
    # add cave to visited
    if cave[0].islower():
        if cave in visited:
            if twice == '':
                twice = cave
            else:
                return
        else:
            visited.add(cave)

    # add to path
    path.append(cave)

    if cave == 'end':
        if twice == '':
            paths_single.append(path.copy())
        paths_twice.append(path.copy())

    else:
        for next in connections[cave]:
            get_pathes(next, connections, paths_single, paths_twice, path, visited, twice)

    path.pop()
    if cave[0].islower():
        if twice == cave:
            twice = ''
        else:
            visited.remove(cave)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
