import numpy as np

def read_input(file_input):
    with open(file_input) as handle:
        start_time = int(handle.readline())
        bus_list = handle.readline().split(',')
    return start_time, bus_list

def question1():
    start_time, bus_list = read_input('inputs/day13.txt')
    min_wait_time = start_time

    for bus in bus_list:
        if bus=='x':
            continue
        else:
            bus = int(bus)
            depart_time = (int(start_time / bus) + 1) * bus
            wait_time = depart_time - start_time
            if wait_time < min_wait_time:
                best_bus = bus
                min_wait_time = wait_time

    print(min_wait_time, best_bus, min_wait_time*best_bus)

def get_all_departures(bus, offset, min_range, max_range):
    next_dep = (int(min_range / bus) + 1) * bus
    return range(next_dep-offset, max_range, bus)


def find_next_departure(bus, offset, current_dep, previous_buses):
    i = 0
    prod = 1
    for b in previous_buses:
        prod *= b

    while True:
        i+=1
        new_value = prod*i + current_dep
        if (prod*i + current_dep + offset) % bus == 0:
            return new_value

def question2():
    '''
    Cannot brute force this. 
    The key is to notice that the intersection of the departure of 2 (or more) buses (with offset) is periodical with a period of bus1 * bus2
    For example, (using the first example), the first time bus 77 leaves and bus 13 leave one minute later is 77, the next is 168 (77+91) and the next is 259 (77+91*2)
    It also works with 3 buses, in the same example, the times that work for bus 7, bus 13+1min and bus 59 + 5 are 3535 + (7*13*59)*J
    We name current_departure[i] the earliest time that verifies our conditions up to bus i.
    Now, all the times verifying the conditions up to bus i-1 are current_departure[i-1] + A*p with p = bus[0]*...*bus[i-1] and A and integer
    And all the times where bus[i] departs are bus[i]*B with B an integer.
    So for a given bus[i] with a necessary offset of k minutes, we need to find 2 integers A and B verifying: 
            bus[i] * B = k + current_departure[i-1] + p*A.
    since A is going to be smaller than B, we iterate over it until we find a value that works. 
    Then current_departure[i] = p*A + current_departure[i-1]
    '''

    _, bus_list = read_input('inputs/day13.txt')
    current_dep = int(bus_list[0])
    previous_buses = [current_dep]
    for offset, bus in enumerate(bus_list[1:]):
        if bus != 'x':
            bus = int(bus)
            current_dep = find_next_departure(bus, offset+1, current_dep, previous_buses)
            previous_buses.append(bus)
    print(current_dep)



if __name__=='__main__':
    question1()
    question2()


