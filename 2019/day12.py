from itertools import combinations
import re
from time import time

INCREMENTS = {0:-3, 1:-1, 2:1, 3:3}

def heapify(arr, n, i): 
    largest = i # set largest as root
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
  
    # See if left child of root exists and is 
    # greater than root 
    if (l < n and arr[i] < arr[l]): 
        largest = l 
  
    # See if right child of root exists and is 
    # greater than root 
    if (r < n and arr[largest] < arr[r]): 
        largest = r 
  
    # Change root, if needed 
    if (largest != i): 
        arr[i],arr[largest] = arr[largest],arr[i] # swap 
  
        # Heapify the root. 
        heapify(arr, n, largest) 
  
# function to sort an array of given size 
def heapSort(arr): 
    n = len(arr) 
  
    # Build a heap. 
    for i in range(n, -1, -1): 
        heapify(arr, n, i) 
  
    # One by one extract elements 
    for i in range(n-1, 0, -1): 
        arr[i], arr[0] = arr[0], arr[i] # swap 
        heapify(arr, i, 0) 
  
# Driver code to test above 
arr = [4, 10, 3, 5, 1]  
heapSort(arr) 
print ("Sorted array is") 
print (arr)

class Universe():
    def __init__(self, moons):
        self.xs = [moon[0] for moon in moons]
        self.ys = [moon[1] for moon in moons]
        self.zs = [moon[2] for moon in moons]
        self.vxs = [0, 0, 0, 0]
        self.vys = [0, 0, 0, 0]
        self.vzs = [0, 0, 0, 0]

    def __repr__(self):
        s = 'pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>\n'
        string = ''
        for i in range(4):
            string += s.format(self.xs[i], self.ys[i], self.zs[i], self.vxs[i], self.vys[i], self.vzs[i])
        return string

    def apply_gravity(self):
        '''To apply gravity, consider every pair of moons. 
        On each axis (x, y, and z), the velocity of each moon changes by 
        exactly +1 or -1 to pull the moons together. 
        For example, if Ganymede has an x position of 3,
        and Callisto has a x position of 5, 
        then Ganymede's x velocity changes by +1 (because 5 > 3) 
        and Callisto's x velocity changes by -1 (because 3 < 5). 
        However, if the positions on a given axis are the same, 
        the velocity on that axis does not change for that pair of moons.'''
        
        # For every axis
        for pos_list, v_list in zip([self.xs, self.ys, self.zs], [self.vxs, self.vys, self.vzs]):
            
            # The planet with the lowest position will have a speed increment of -3 (-1 for each other planet)
            # The second lowest planet has a speed increment of -1 (-1 for the 2 higher and +1 for the lowest) 
            # The third has an increment of +1 and the last of +3 (see definition of INCREMENTS).
            # If their are some equalities, we correct after
            for i in range(4):
                
                v_list += len(pos_list[pos_list>pos_list[i]]) * 2 - 3
 

    def apply_velocity(self):
        for pos_list, v_list in zip([self.xs, self.ys, self.zs], [self.vxs, self.vys, self.vzs]):
            for i in range(4):
                pos_list[i] += v_list[i]

    def run_step(self):
        start = time()
        self.apply_gravity()
        m = time()
        self.apply_velocity()
        end = time()
        # print('Gravity:', m-start)
        # print('Velocity:', end-m)

    def get_energy(self):
        total = 0
        for i in range(4):
            potential = abs(self.xs[i]) + abs(self.ys[i]) + abs(self.zs[i])
            kinetic = abs(self.vxs[i]) + abs(self.vys[i]) + abs(self.vzs[i])
            total += potential + kinetic
        return total

    def get_state(self):
        string = ''
        for pos_list, v_list in zip([self.xs, self.ys, self.zs], [self.vxs, self.vys, self.vzs]):
            string += '{}|{}|{}|{}|{}|{}|{}|{}'.format(*pos_list, *v_list)
        return string



input_re = re.compile('<x=([-0-9]+), y=([-0-9]+), z=([-0-9]+)>')
def parse_input(input_file):
    moons = []
    with open(input_file, 'r') as handle:
        for line in handle.readlines():
                match = input_re.search(line)
                moons.append([int(match.group(1)), int(match.group(2)), int(match.group(3))])
    return moons


if __name__=='__main__':

    moons = parse_input('inputs/examples/day12.txt')
    universe = Universe(moons)
    
    n = 0
    start = time()
    for i in range(10):
        print('After {} steps:'.format(i))
        print(universe)
        start = time()
        # prev_states.add(current_state)
        m1 = time()
        universe.run_step()
        m2 = time()
        # print('Add', m1-start)
        # print('Run', m2-m1)


 
    print('Energy', universe.get_energy())
    # print('Number of rounds before returning to a previous state:', n)




