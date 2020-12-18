import numpy as np
import pandas as pd

N = 1000

def draw_cables(c1, c2):
    n_cols = N
    n_rows = N
    grid = np.zeros((n_rows, n_cols), dtype=int)
    central_port = [0, 0]

    candidates = []
    for cable, score in zip([c1, c2], [1, 10]):
        current_pos = list(central_port)
        for instruction in cable.split(','):
            direction = instruction[0]
            n = int(instruction[1:])

            if direction=='R':
                # If it overflows, double the number of columns by adding them to the right.
                if current_pos[1] + n + 1 > n_cols:
                    print('Adding columns to the right')
                    new_cols = np.zeros((n_rows, n_cols), dtype=int)
                    grid = np.concatenate((grid,new_cols), axis=1)
                    n_cols =  n_cols * 2
                
                # Actually draw the cable
                grid[current_pos[0], current_pos[1]+1:current_pos[1]+n+1] += score
                current_pos[1] +=  n
            
            elif direction=='L':
                # If it overflows, double the number of columns by adding them to the left.
                # And don't forget to update the position of the central port and the curent position
                if current_pos[1] - n <= 0:
                    print('Adding columns to the left')
                    new_cols = np.zeros((n_rows, n_cols), dtype=int)
                    grid = np.concatenate((new_cols, grid), axis=1)
                    current_pos[1] += n_cols
                    central_port[1] += n_cols
                    n_cols =  n_cols * 2

                # Actually draw the cable
                grid[current_pos[0], current_pos[1]-n:current_pos[1]] += score
                
                current_pos[1] -=  n

            elif direction=='U':
                # If it overflows, double the number of coluns by adding them at the top
                # And don't forget to update the position of the central port and the curent position
                if current_pos[0] - n <= 0:
                    print('Adding rows to the top')
                    new_rows = np.zeros((n_rows, n_cols), dtype=int)
                    grid = np.append(new_rows, grid, 0)
                    current_pos[0] += n_rows
                    central_port[0] += n_rows
                    n_rows = n_rows * 2

                # Actually draw the cable
                grid[current_pos[0]-n:current_pos[0], current_pos[1]] += score
                current_pos[0] -=  n
            
            elif direction=='D':
                # If it overflows, double the number of coluns by adding them at the bottom
                if current_pos[0] + n + 1 > n_rows:
                    print('Adding rows to the bottom')
                    new_rows = np.zeros((n_rows, n_cols), dtype=int)
                    grid = np.append(grid, new_rows, 0)
                    n_rows = n_rows * 2

                # Actually draw the cable
                grid[current_pos[0]+1:current_pos[0]+n+1, current_pos[1]] += score
                current_pos[0] +=  n 

    return grid, central_port

def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def find_closest_intersection(c1, c2):
    grid, center = draw_cables(c1, c2)
    # Explore the grid by starting from the central port and expanding the radius 
    for r in range(1, grid.shape[0] + grid.shape[1]):
        print('Exploring radius: '+str(r))
        for x in np.arange(-r, r):
            for y in [r-(abs(x)), -(r-abs(x))]:
                # print(x, y, grid[center[0]+x][center[1]+y])
                # input('?')
                if grid[center[0]+x][center[1]+y]==11:
                    return r  

def get_xy_incr(direction):
    if direction == 'R':
        y_incr = 0
        x_incr = 1
    elif direction == 'L':
        y_incr = 0
        x_incr = -1
    elif direction == 'U':
        y_incr = -1
        x_incr = 0
    elif direction == 'D':
        y_incr = 1
        x_incr = 0
    return x_incr, y_incr

def get_cable_distance(cable, position, center):
    cable_dist = 0
    current_pos = list(center)
    for instruction in cable.split(','):
        direction = instruction[0]
        n = int(instruction[1:])
        x_incr, y_incr = get_xy_incr(direction)

        for _ in range(n):
            cable_dist += abs(x_incr) + abs(y_incr)
            current_pos[0] += y_incr
            current_pos[1] += x_incr
            if current_pos[0]==position[0] and current_pos[1]==position[1]:
                return cable_dist

def find_delay_intersection(c1, c2):
    grid, center = draw_cables(c1, c2)
    min_dist = N**2
    intersection = (None, None)
    # Explore the path of the first cable, when we find an intersection, compute the distance and see if it's better
    current_pos = list(center)
    c1_dist = 0
    for instruction in c1.split(','):
        direction = instruction[0]
        n = int(instruction[1:])
        x_incr, y_incr = get_xy_incr(direction)

        for _ in range(n):
            c1_dist += 1
            current_pos[0] += y_incr
            current_pos[1] += x_incr
            if grid[current_pos[0], current_pos[1]]==11:
                c2_dist = get_cable_distance(c2, current_pos, center)
                total_dist = c1_dist + c2_dist
                if total_dist < min_dist:
                    min_dist = total_dist
                    intersection = current_pos

        if c1_dist > min_dist:
            return min_dist

    return min_dist

def run_tests1():
    c1= 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    c2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    assert find_closest_intersection(c1, c2) == 159
    c1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    c2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    assert find_closest_intersection(c1, c2) == 135

def run_tests2():
    c1= 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    c2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    assert find_delay_intersection(c1, c2) == 610
    c1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    c2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    assert find_delay_intersection(c1, c2) == 410    

def question1():
    with open('inputs/day03.txt') as handle:
            c1 = handle.readline()
            c2 = handle.readline()
            min_dist = find_closest_intersection(c1, c2)
            print(min_dist) 

def question2():
    with open('inputs/day03.txt') as handle:
            c1 = handle.readline()
            c2 = handle.readline()
            min_dist = find_delay_intersection(c1, c2)
            print(min_dist) 

if __name__=='__main__':
    run_tests1()
    run_tests2()
    question1()
    question2()
    
 