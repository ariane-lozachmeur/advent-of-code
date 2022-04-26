import numpy as np
import pandas as pd
from fractions import Fraction
from copy import deepcopy

def get_asteroids(this_map, x_step, y_step, target_pos):
    asteroids = [None, None] # First for before crossed target, second for after
    max_x = len(this_map[0])
    max_y = len(this_map)
    crossed_target = False
    # explore the left on the target (assuming steps are positive) 
    # and stop at the first hit
    ax = target_pos[0] + x_step
    ay = target_pos[1] + y_step
    while ax < max_x and ay < max_y and ax>=0 and ay>=0 and asteroids[0] is None:
        if this_map[ay][ax] == '#':
            asteroids[0] = (ax, ay)
        ax += x_step
        ay += y_step

    # explore the right on the target (assuming steps are positive) 
    # and stop at the first hit
    ax = target_pos[0] - x_step
    ay = target_pos[1] - y_step
    while ax < max_x and ay < max_y and ax>=0 and ay>=0 and asteroids[1] is None:
        if this_map[ay][ax] == '#':
            asteroids[1] = (ax, ay)
        ax -= x_step
        ay -= y_step

    return asteroids

def get_angle(position, angle_x, angle_y):
    if position[0] == angle_x:
        x_step = 0
        y_step = 1
        angle = Fraction(-1/10000)
    elif position[1] == angle_y:
        x_step = 1
        y_step = 0
        angle = 0
    else:
        big_x_step = (position[0]-angle_x)
        big_y_step = (position[1]-angle_y)
        f = Fraction(big_x_step, big_y_step)
        x_step = f.numerator
        y_step = f.denominator
        angle = f

    return angle, x_step, y_step

def count_asteroids(this_map, position):
    hits = []
    explored_angles = []

    for x in range(len(this_map[0])): 
        for y in range(len(this_map)):
            new_angle, x_step, y_step = get_angle(position, x, y)
            if new_angle not in explored_angles:
                # print(x, y, new_angle)
                explored_angles.append(new_angle)
                new_hits = get_asteroids(this_map, x_step, y_step, position)
                hits += new_hits
    # Get unique hits
    hits = [h for i, h in enumerate(hits) if not h is None and h not in hits[:i]]
    return hits, len(hits)

def generate_sorted_angles(this_map, position):
    explored_angles = []
    steps = {}
    for x in range(len(this_map[0])): 
        for y in range(len(this_map)):
            # laser starts pointing up so add the position
            # use a simple congruence to loop around
            real_x = (x + position[0]) % len(this_map[0])
            real_y = (y + position[1]) % len(this_map)
            new_angle, x_step, y_step = get_angle(position, x, y)
            if new_angle not in explored_angles:
                explored_angles.append(new_angle)
                steps[new_angle] = (x_step, y_step)
    pos_angles = sorted([f for f in explored_angles if f>0], reverse=True)
    neg_angles = sorted([f for f in explored_angles if f<0], reverse=True)
    return neg_angles, [0] + pos_angles, steps

def destroy_on_angle(this_map, x_step, y_step, target_pos, direction):
    # direction is +1 or -1
    max_x = len(this_map[0])
    max_y = len(this_map)
    # explore the left on the target (assuming steps are positive) 
    # and stop at the first hit
    ax = target_pos[0] + direction * x_step
    ay = target_pos[1] + direction * y_step

    while ax < max_x and ay < max_y and ax>=0 and ay>=0:
        if this_map[ay][ax] == '#':
            return (ax, ay)
        ax += direction * x_step
        ay += direction * y_step
    return None

def perform_quarter_turn(this_map, destroyed_map, current_n, position, angles, steps, direction):
    n = current_n
    for angle in angles:
        x_step, y_step = steps[angle]
        # print(angle, x_step, y_step)
        destroyed_asteroid = destroy_on_angle(this_map, x_step, y_step, position, direction)
        if destroyed_asteroid is not None:
            # print(angle, steps[angle], n)
            destroyed_map[destroyed_asteroid[1]][destroyed_asteroid[0]] = n
            if n == 200:
                print('Answer', destroyed_asteroid[0] * 100 + destroyed_asteroid[1])
            this_map[destroyed_asteroid[1]][destroyed_asteroid[0]] = '.'
            n += 1
    return n

def perform_full_turn(this_map, destroyed_map, current_n, position, neg_angles, pos_angles, steps):
    # Upper right quadrant
    current_n = perform_quarter_turn(this_map, destroyed_map, current_n, position, neg_angles, steps, -1)

    # Lower right quadrant
    current_n = perform_quarter_turn(this_map, destroyed_map, current_n, position, pos_angles, steps, 1)

    # Lower left quadrant
    current_n = perform_quarter_turn(this_map, destroyed_map, current_n, position, neg_angles, steps, 1)

    # Upper left quadrant
    current_n = perform_quarter_turn(this_map, destroyed_map, current_n, position, pos_angles, steps, -1)
    return current_n


def detroy_asteroids(this_map, position, neg_angles, pos_angles, steps):
    n = 1
    destroyed_map = deepcopy(this_map)
    while n < 210:
        n = perform_full_turn(this_map, destroyed_map, n, position, neg_angles, pos_angles, steps)

    return this_map, destroyed_map

def show_hits_on_map(space, hits, position):
    for y in range(len(space)):
        row = ''
        for x in range(len(space[y])):
            if (x, y) == position:
                row += 'O'
            elif (x, y) in hits:
                row += '@'
            else:
                row += space[y][x]
        print(row)

def find_best_pos(n_hits):
    max_visible = 0
    best_pos = None
    for x in range(len(n_hits[0])):
        for y in range(len(n_hits)):
            if n_hits[y][x] > max_visible:
                max_visible = n_hits[y][x]
                best_pos = (x, y)
    return best_pos, max_visible

def question1():
    space = []
    with open('inputs/day10.txt') as handle:
        for l in handle.readlines():
            space.append(list(l.strip('\n')))

    print(pd.DataFrame(space))
    n_hits = []
    for y in range(len(space)):
        row = []
        for x in range(len(space[0])):
            if space[y][x] == '#':
                hits, n = count_asteroids(space, (x, y))
                row.append(n)
            else:
                row.append(0)
        n_hits.append(row)
    print(pd.DataFrame(n_hits))
    print(find_best_pos(n_hits))    


if __name__ == '__main__':

    space = []
    with open('inputs/day10.txt') as handle:
        for l in handle.readlines():
            space.append(list(l.strip('\n')))

    best_pos = (13, 17)
    neg_angles, pos_angles, steps = generate_sorted_angles(space, best_pos)
    this_map, destruction_map = detroy_asteroids(space, best_pos, neg_angles, pos_angles, steps)
    print(pd.DataFrame(destruction_map))
    print(pd.DataFrame(space))
    