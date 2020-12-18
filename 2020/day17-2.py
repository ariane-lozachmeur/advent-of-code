import pandas as pd
from copy import copy

class Bag():
    def __init__(self, input_file):
        with open(input_file, 'r') as handle:
            lines = handle.readlines()
        self.dimensions = {'x':[0, len(lines[0])-1], 'y':[0, len(lines)], 'z':[0, 1], 'w':[0, 1]}
        
        self.map = []
        for l in lines:
            l = l.strip('\n')
            self.map.append(list(l))
        # map(x, y, z, w) = self.map[w][z][y][x]
        self.map = [[self.map]]

    def __str__(self):
        string = ''
        for i, hyplerplane in enumerate(self.map):
            for j, plane in enumerate(hyplerplane):
                string += 'Plane w={}, z={}\n'.format(self.dimensions['w'][0]+i, self.dimensions['z'][0]+j)
                for row in plane:
                    string += ''.join(row)+'\n'
        return string

    def get_range(self, dim):
        return self.dimensions[dim][1] - self.dimensions[dim][0]

    def add_padding(self):
        new_x_range = self.dimensions['x'][1] - self.dimensions['x'][0] + 2
        new_y_range = self.dimensions['y'][1] - self.dimensions['y'][0] + 2
        new_z_range = self.dimensions['z'][1] - self.dimensions['z'][0] + 2

        for dim in ['x', 'y', 'z', 'w']:
            self.dimensions[dim][0] -= 1
            self.dimensions[dim][1] += 1

        new_map = []
        for hyplerplane in self.map:
            new_hyperplane = []
            for plane in hyplerplane:
                # Padding the Xs
                new_plane = []
                for row in plane:
                    new_row = ['.'] + row + ['.']
                    new_plane.append(new_row)
                # Padding the Ys
                new_plane = [['.' for _ in range(new_x_range)]] + new_plane + [['.' for _ in range(new_x_range)]]
                # print(new_plane)
                new_hyperplane.append(new_plane)
            # Padding the Zs
            new_hyperplane = [[['.' for _ in range(new_x_range)] for _ in range(new_y_range)]] + new_hyperplane + [[['.' for _ in range(new_x_range)] for _ in range(new_y_range)]]
            new_map.append(new_hyperplane)
        # Padding the Ws
        self.map = [[[['.' for _ in range(new_x_range)] for _ in range(new_y_range)] for _ in range(new_z_range)]] + new_map + [[[['.' for _ in range(new_x_range)] for _ in range(new_y_range)] for _ in range(new_z_range)]]

    def get_status(self, pos):
        x, y, z, w = pos
        if 0 <= w < len(self.map):
            hyperplane = self.map[w]
            if 0 <= z < len(hyperplane):
                plane = hyperplane[z]
                if 0 <= y < len(plane):
                    row = plane[y]
                    if 0 <= x < len(row):
                        return row[x]
        return '.'

    def count_active_neigbors(self, pos):
        x, y, z, w = pos
        count = 0
        for neigh_x in [x-1, x, x+1]:
            for neigh_y in [y-1, y, y+1]:
                for neigh_z in [z-1, z, z+1]:
                    for neigh_w in [w-1, w, w+1]:
                        if neigh_x != x or neigh_y != y or neigh_z != z or neigh_w != w:
                            status = self.get_status((neigh_x, neigh_y, neigh_z, neigh_w))
                            count += status == '#'
        return count

    def update_cube(self, pos):
        x, y, z, w = pos
        count = self.count_active_neigbors(pos)
        try:
            cube = self.map[w][z][y][x]
        except:
            print(pos)
            raise
        if cube == '#':
            if not (1 < count < 4):
                return '.'
        elif count == 3:
            return '#'
        return None

    def run_cycle(self):
        self.add_padding()
        print('New dimensions: {}'.format(self.dimensions))
        updates = []
        for w in range(self.get_range('w')):
            for z in range(self.get_range('z')):
                for y in range(self.get_range('y')):
                    for x in range(self.get_range('x')):
                        update = self.update_cube((x, y, z, w))
                        if not update is None:
                            updates.append(((x, y, z, w), update))
        for ((x, y, z, w), update) in updates:
            self.map[w][z][y][x] = update


    def count_active(self):
        count = 0
        for hyperplane in self.map:
            for plane in hyperplane:
                for row in plane:
                    count += row.count('#')
        return count


if __name__=='__main__':

    bag = Bag('inputs/day17.txt')
    # print(bag)
    for i in range(6):
        print('Run cycle {}'.format(i+1))
        bag.run_cycle()
        # print(bag)
        # input('Continue?')

    print(bag.count_active())

