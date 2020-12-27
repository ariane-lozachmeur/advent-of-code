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

from time import time

class LinkedList():
    def __init__(self, n_cups, input_str):
        self.head = None
        self.n_cups = n_cups
        self.value_to_cup = {}

        current_cup = Cup(int(input_str[0]))
        self.head = current_cup
        self.value_to_cup[int(input_str[0])] = current_cup

        for c in input_str[1:]:
            new_cup = Cup(int(c))
            current_cup.link_to(new_cup)
            self.value_to_cup[int(c)] = new_cup
            current_cup = new_cup
        
        # For question 2, add all the additional cups
        for c in range(len(input_str), n_cups):
            new_cup = Cup(int(c+1))
            current_cup.link_to(new_cup)
            self.value_to_cup[int(c+1)] = new_cup
            current_cup = new_cup  

        # Make it circular
        current_cup.next = self.head


    def __repr__(self):
        initial_node = self.head
        node = self.head
        nodes = [str(node.value)]      
        node = node.next  
        while node is not None and node != initial_node:
            nodes.append(str(node.value))
            node = node.next
        return " -> ".join(nodes)

    def pick_cups(self):
        head = self.head
        cup1 = self.head.next
        cup2 = cup1.next
        cup3 = cup2.next
        self.head.next = cup3.next
        cup3.next = None
        return [cup1, cup2, cup3]

    def find_destination_cup(self, picked_cups):
        picked_cups_values = [c.value for c in picked_cups]
        value = self.head.value - 1
        if value == 0:
            value = self.n_cups
        
        while value in picked_cups_values:
            value -= 1
            if value == 0:
                value = self.n_cups

        return self.value_to_cup[int(value)]

    def replace_cups(self, destination_cup, picked_cups):
        picked_cups[2].next = destination_cup.next
        destination_cup.next = picked_cups[0]

    def play_round(self):
        # t1 = time()
        picked_cups = self.pick_cups()
        # t2 = time()
        destination_cup = self.find_destination_cup(picked_cups)
        # t3 = time()
        # print('Pick up', picked_cups)
        # print('Destination', destination_cup)
        self.replace_cups(destination_cup, picked_cups)
        # t4 = time()
        # print('Pick', t2-t1)
        # print('Find destination', t3-t2)
        # print('Replace', t4-t3)
        self.head = self.head.next

    def output_final_string(self):
        string = ''
        current = self.head
        # Find the 1
        while current.value != 1:
            current = current.next

        # Write the string until we hit 1 again
        current = current.next
        while current.value != 1:
            string += str(current.value)
            current = current.next
        return string

    def output_2_cups(self):
        current = self.head
        # Find the 1
        while current.value != 1:
            current = current.next
        
        # print(current)
        cup1 = current.next
        cup2 = cup1.next
        return [cup1.value, cup2.value, cup1.value*cup2.value] 

class Cup():
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return '({})'.format(self.value)

    def link_to(self, this_next):
        self.next = this_next


if __name__=='__main__':
    # my_input = '389125467' # test input
    my_input = '394618527'
    N_ROUNDS = 10000000
    N_CUPS = 1000000

    # N_CUPS = 10
    # N_ROUNDS = 1
    llist = LinkedList(N_CUPS, my_input)

    for n in range(N_ROUNDS):
        # start = time()
        # print('--- Round {} ---'.format(n+1))
        # print(llist)
        llist.play_round()
        # end = time()
        # print('Time for 1 rounds (in s)', end-start)
            # print('Time for all rounds (in minutes)', (end-start)*10000/60)


    print(llist.output_2_cups())
    # print(llist.output_final_string())
