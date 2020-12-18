from copy import copy

def question1():
    diffs = []
    low = 0
    n1 = 0
    n2 = 0
    n3 = 0
    for high in voltages:
        diffs.append(high - low)
        n1 +=  (high - low) == 1
        n2 +=  (high - low) == 2
        n3 +=  (high - low) == 3
        low = high

    print(len(diffs))
    print(n1)
    print(n2)
    print(n3)
    print(n1*n3)



def count_next(voltages, current_pos, max_diff=3):
    diff = 0
    direct_count = 0
    this_volt = voltages[current_pos]
    i = current_pos-1
    if current_pos == 0:
        # print(current_pos, this_volt, 1)
        return 1

    while diff < 4 and i >= 0:
        diff = this_volt - voltages[i]
        if diff < 4:
            if i in COUNTED.keys():
                c = COUNTED[i]
            else:
                c = count_next(voltages, i)
                COUNTED[i] = c
            direct_count += c
        i -= 1

    # print(current_pos, this_volt, direct_count)
    return direct_count


if __name__=='__main__':
    voltages = [16,10,15,5,1,11,7,19,6,12,4]
    with open('inputs/day10.txt','r') as handle:
        voltages = [int(l.strip('\n')) for l in handle.readlines()]

    
    voltages = sorted(voltages)
    COUNTED = {}
    # print(voltages)
    device_volt = voltages[-1]+3
    voltages.append(device_volt)
    voltages = [0]+voltages
    current_pos = len(voltages)-1
    total = count_next(voltages, current_pos)
    print(total)
