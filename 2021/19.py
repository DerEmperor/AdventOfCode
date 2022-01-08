import sys
import time
import numpy as np
from scanf import scanf


def get_permutation(beacon, permutation):
    x, y, z = beacon
    if permutation == 0:
        return x, y, z
    elif permutation == 1:
        return -y, x, z
    elif permutation == 2:
        return -x, -y, z
    elif permutation == 3:
        return y, -x, z

    elif permutation == 4:
        return z, y, -x
    elif permutation == 5:
        return -y, z, -x
    elif permutation == 6:
        return -z, -y, -x
    elif permutation == 7:
        return y, -z, -x

    elif permutation == 8:
        return -x, y, -z
    elif permutation == 9:
        return y, -x, -z
    elif permutation == 10:
        return x, -y, -z
    elif permutation == 11:
        return -y, x, -z

    elif permutation == 12:
        return -z, y, x
    elif permutation == 13:
        return -y, -z, x
    elif permutation == 14:
        return z, -y, x
    elif permutation == 15:
        return y, z, x

    elif permutation == 16:
        return x, z, -y
    elif permutation == 17:
        return -z, x, -y
    elif permutation == 18:
        return -x, -z, -y
    elif permutation == 19:
        return z, -x, -y

    elif permutation == 20:
        return x, -z, y,
    elif permutation == 21:
        return z, -x, y
    elif permutation == 22:
        return -x, z, y,
    elif permutation == 23:
        return -z, x, y
    else:
        print("ERROR")
        sys.exit(1)


def main():
    with open('inputs/19_input_test.txt', 'r') as file:
        input_ = file.readlines()

    beacons_by_scanners = []

    scanner = -1

    for line in input_:
        if line == '\n':
            continue

        if line[0:3] == '---':
            scanner += 1
            beacons_by_scanners.append([])
            continue

        coord = scanf('%d,%d,%d\n', line)
        beacons_by_scanners[scanner].append(coord)

    all_beacons = set(beacons_by_scanners[0])
    beacons_by_scanners = beacons_by_scanners[1:]

    while len(beacons_by_scanners) > 0:
        for beacons in beacons_by_scanners:
            found = False
            for permutation in range(24):
                for right_beacon in all_beacons:
                    for new_beacon in beacons:
                        new_beacon = get_permutation(new_beacon, permutation)
                        offset = (
                            new_beacon[0] - right_beacon[0], new_beacon[1] - right_beacon[1],
                            new_beacon[2] - right_beacon[2])
                        counter = 0
                        for beacon in beacons:
                            beacon = get_permutation(beacon, permutation)
                            beacon = (beacon[0] + offset[0], beacon[1] + offset[1], beacon[2] + offset[2])

                            if beacon in all_beacons:
                                counter += 1

                            if counter >= 12:
                                # found
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break

            if found:
                # add beacons to all_beacons
                print(offset)
                for beacon in beacons:
                    beacon = get_permutation(beacon, permutation)
                    beacon = (beacon[0] + offset[0], beacon[1] + offset[1], beacon[2] + offset[2])

                    all_beacons.add(beacon)
                beacons_by_scanners.remove(beacons)
                break
        if not found:
            print("ERROR")
            sys.exit(1)


    print(len(all_beacons))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
