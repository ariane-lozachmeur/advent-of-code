from itertools import combinations
import re
from time import time

class Universe():
    def __init__(self, moons, names):
        self.moons = {}
        for name, moon in zip(names,moons):
            self.moons[name] = Moon(moon, name)

    def __repr__(self):
        string = ''
        for name, moon in self.moons.items():
            string += name + ' : ' + str(moon) + '\n'
        return string

    def apply_gravity(self):
        '''To apply gravity, consider every pair of moons. '''
        pairs = combinations(self.moons.keys(), 2)
        for p1, p2 in pairs:
            self.moons[p1].apply_gravity(self.moons[p2])

    def apply_velocity(self):
        for moon in self.moons.values():
            moon.move()

    def run_step(self):
        start = time()
        self.apply_gravity()
        m = time()
        self.apply_velocity()
        end = time()
        print('Gravity:', m-start)
        print('Velocity:', end-m)

    def get_energy(self):
        total = 0
        for moon in self.moons.values():
            total += moon.energy()
        return total

    def get_state(self):
        string = ''
        for moon in self.moons.values():
            string+=str(moon)
        return string


class Moon():
    def __init__(self, pos, name):
        self.name = name
        self.pos = pos
        self.v = [0, 0, 0]

    def __repr__(self):
        return f'pos <x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}> vel=<x={self.v[0]}, y={self.v[1]}, z={self.v[2]}>'

    def apply_gravity(self, other_moon):
        '''On each axis (x, y, and z), the velocity of each moon changes by 
        exactly +1 or -1 to pull the moons together. 
        For example, if Ganymede has an x position of 3,
        and Callisto has a x position of 5, 
        then Ganymede's x velocity changes by +1 (because 5 > 3) 
        and Callisto's x velocity changes by -1 (because 3 < 5). 
        However, if the positions on a given axis are the same, 
        the velocity on that axis does not change for that pair of moons.'''

        for dim in range(3):
            if self.pos[dim] < other_moon.pos[dim]:
                self.v[dim]  += 1
                other_moon.v[dim] += -1
            elif self.pos[dim] > other_moon.pos[dim]:
                self.v[dim] += -1
                other_moon.v[dim] += 1

    def move(self):
        '''Simply add the velocity of each moon to its own position. 
        For example, if Europa has a position of x=1, y=2, z=3 and a velocity 
        of x=-2, y=0,z=3, then its new position would be x=-1, y=2, z=6. 
        This process does not modify the velocity of any moon.'''
        for dim in range(3):
            self.pos[dim] += self.v[dim]

    def energy(self):
        '''The total energy for a single moon is its potential 
        energy multiplied by its kinetic energy. 
        A moon's potential energy is the sum of the absolute
        values of its x, y, and z position coordinates. 
        A moon's kinetic energy is the sum of the absolute
        values of its velocity coordinates'''

        potential = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kinetic = abs(self.v[0]) + abs(self.v[1]) + abs(self.v[2])
        return potential * kinetic

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
    names = ['Io', 'Europa', 'Ganymede', 'Callisto']
    universe = Universe(moons, names)
    
    print(universe)
    prev_states = set()
    current_state = universe.get_state()
    n = 0
    start = time()
    while current_state not in prev_states and n < 100000:
        start = time()
        prev_states.add(current_state)
        m1 = time()
        universe.run_step()
        m2 = time()
        current_state = universe.get_state()
        end = time()
        print('Add', m1-start)
        print('Run', m2-m1)
        print('Get state', end-m2)

        t1 = time()
        b = current_state in prev_states
        t2 = time()
        print('Test', t2-t1)

        n+=1
        if n % 10000 == 9999:
            print(n)
            end = time()
            print('Time to run 10000 rounds:', end-start)
            start = time()
        # if n ==2773:
            # print(current_state)
            # print(prev_states)

 
    print('Number of rounds before returning to a previous state:', n)




