import time

hex2bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def main():
    with open('inputs/16_input.txt', 'r') as file:
        input_ = file.readlines()
    data = ''.join([hex2bin[x] for x in input_[0][:-1]])

    print(input_[0][:-1])
    print(data)

    version, number, end = evaluate_data(data)

    print(version)
    print(number)


def evaluate_data(data):
    version = int(data[:3], 2)
    type_id = int(data[3:6], 2)

    if type_id == 4:
        # literal value

        number, end = evaluate_number(data[6:])
        end += 7
        return version, number, end

    else:
        # operator
        if data[6] == '0':
            # 7 + 15 = 22
            length_packages = int(data[7:22], 2)
            sub_packets = data[22:22 + length_packages]

            versions, numbers = evaluate_sub_packets_length(sub_packets)
            end = 22 + length_packages

        else:
            number_sub_packets = int(data[7:7 + 11], 2)

            versions, numbers, end = evaluate_sub_packets_number(data[18:], number_sub_packets)
            end += 18

    version += sum(versions)
    number = apply(type_id, numbers)

    return version, number, end


def evaluate_number(data):
    i = 0
    last = False
    number = ''
    while not last:
        number = '{}{}'.format(number, data[i + 1:i + 1 + 4])
        last = data[i] == '0'
        i += 5
    number = int(number, 2)
    end = i - 1
    return number, end


def evaluate_sub_packets_length(data):
    versions = []
    numbers = []

    start = 0
    last = False
    while not last:
        version, number, end = evaluate_data(data[start:])

        versions.append(version)
        numbers.append(number)

        start += end
        last = start == len(data)

    return versions, numbers


def evaluate_sub_packets_number(data, number_sub_packets):
    versions = []
    numbers = []

    start = 0
    end = 0
    for i in range(number_sub_packets):
        version, number, number_end = evaluate_data(data[start:])

        versions.append(version)
        numbers.append(number)

        start += number_end
        end += number_end

    return versions, numbers, end


def apply(type_id, numbers):
    if type_id == 0:
        return sum(numbers)
    if type_id == 1:
        return mul(numbers)
    if type_id == 2:
        return min(numbers)
    if type_id == 3:
        return max(numbers)
    if type_id == 5:
        return int(numbers[0] > numbers[1])
    if type_id == 6:
        return int(numbers[0] < numbers[1])
    if type_id == 7:
        return int(numbers[0] == numbers[1])

    print("ERROR")
    return 0


def mul(list_):
    res = 1
    for i in list_:
        res *= i
    return res


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
