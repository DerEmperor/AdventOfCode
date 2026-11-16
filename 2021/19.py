import sys
import time


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
        return y, x, -z
    elif permutation == 10:
        return x, -y, -z
    elif permutation == 11:
        return -y, -x, -z

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
        return z, x, y
    elif permutation == 22:
        return -x, z, y,
    elif permutation == 23:
        return -z, -x, y
    else:
        print("ERROR")
        sys.exit(1)


def main():
    with open('inputs/19_input.txt', 'r') as file:
        input_ = file.readlines()

    beacons_by_scanners = []

    for line in input_:
        line = line.strip()
        if not line:
            continue

        if line.startswith('---'):
            beacons_by_scanners.append([])
            continue

        coord = tuple(int(x) for x in line.split(','))
        beacons_by_scanners[-1].append(coord)

    scanner_positions = [(0, 0, 0)]
    all_beacons = set(beacons_by_scanners[0])
    beacons_by_scanners = beacons_by_scanners[1:]

    while beacons_by_scanners:
        for beacons in beacons_by_scanners:
            found = False
            for permutation in range(24):
                rotated_beacons = [get_permutation(b, permutation) for b in beacons]
                for rotated in rotated_beacons:
                    for right_beacon in all_beacons:
                        offset = (
                            right_beacon[0] - rotated[0], right_beacon[1] - rotated[1],
                            right_beacon[2] - rotated[2])
                        counter = 0
                        for beacon in rotated_beacons:
                            if (beacon[0] + offset[0], beacon[1] + offset[1],
                                beacon[2] + offset[2]) in all_beacons:
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
                for beacon in rotated_beacons:
                    all_beacons.add(
                        (beacon[0] + offset[0], beacon[1] + offset[1], beacon[2] + offset[2]))
                scanner_positions.append(offset)
                beacons_by_scanners.remove(beacons)
                break
        if not found:
            print("ERROR")
            sys.exit(1)

    print('part1', len(all_beacons))

    part2 = 0
    for p1 in scanner_positions:
        for p2 in scanner_positions:
            dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
            if dist > part2:
                part2 = dist
    print('part2', part2)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
