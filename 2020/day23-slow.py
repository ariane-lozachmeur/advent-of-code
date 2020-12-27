'''The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were 32415, there would be five cups in the circle; going clockwise around the circle from the first cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.

Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.

Each move, the crab does the following actions:

1. The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; 
cup spacing is adjusted as necessary to maintain the circle.

2. The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
If this would select one of the cups that was just picked up, the crab will keep subtracting one until 
it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest 
value on any cup's label, it wraps around to the highest value on any cup's label instead.

3. The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. 
They keep the same order as when they were picked up.
The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

After the crab is done, what order will the cups be in? Starting after the cup labeled 1, 
collect the other cups' labels clockwise into a single string with no extra characters; 
each number except 1 should appear exactly once. In the above example, after 10 moves, 
the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374. 
If the crab were to complete all 100 moves, the order after cup 1 would be 67384529.
'''

'''-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7 
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7 
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1 
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6 
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1 
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7 
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6 
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5 
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6 
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6'''

import pandas as pd
from time import time

N_CUPS = 1000000

def get_max(cups):
    return pd.Series(list(cups)).apply(int).max()

def get_index(index):
    if index < N_CUPS:
        return index
    else:
        return  index - N_CUPS

def remove_cups(current_index, cups):
    i1 = get_index(current_index+1)
    i2 = get_index(current_index+4)
    if i1 < i2:
        moved_cups = cups[i1:i2]
        cups = cups[:i1] + cups[i2:]
    else:
        moved_cups = cups[i1:] + cups[:i2]
        cups = cups[i2:i1]
    
    return moved_cups, cups

def move_cups(cups, current_index):
    # Part 1: removing the 3 cups
    start = time()
    current_cup = cups[current_index]
    # print('current cup', current_cup, 'index', current_index)
    moved_cups, cups = remove_cups(current_index, cups)
    end = time()
    print('Part 1:', end-start)

    # print('pick up', moved_cups)    
    # Part 2: finding the destination
    start = time()
    destination_index = None
    destination_value = current_cup
    while destination_index is None:
        destination_value = int(destination_value)-1
        if int(destination_value) < 0:
            destination_value = get_max(cups)
        if destination_value in cups:
            destination_index = cups.index(destination_value)
    end = time()
    print('Part 2:', end-start)

    # print('destination', destination_value)
    # Part 3: adding back the cups
    start = time()
    cups = cups[:destination_index+1] + moved_cups + cups[destination_index+1:]
    end = time()
    print('Part 3:', end-start)

    # Part 4: adjust current_index
    start = time()
    current_index = cups.index(current_cup)
    current_index = current_index+1 if current_index+1 < N_CUPS else 0
    end = time()
    print('Part 4:', end-start)
    return cups, current_index

def get_final_string(cups):
    start = cups.index('1')
    return cups[start+1:] + cups[:start]

def get_inital_setup(input_str, N_CUPS):
    l = [int(s) for s in input_str]
    for i in range(len(l)+1, N_CUPS):
        l.append(i)
    return l


if __name__=="__main__":

    cups = '389125467'
    # cups = '394618527'
    cups = get_inital_setup(cups, N_CUPS)
    # print(cups)
    n_moves = 100
    # n_moves = 10000000
    start = time()
    current_index = 0
    for n in range(n_moves):
        # print('Round', n+1)
        # print(list(cups))
        cups, current_index = move_cups(cups, current_index)
        # print('----')

    index = cups.index(1)
    # print(cups[index+1])
    # print(cups[index+2])
    # print(cups[index+1]*cups[index+2])

    end = time()
    print(end-start)

    # print(list(cups))
    # print(get_final_string(cups))
