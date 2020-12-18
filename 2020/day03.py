import pandas as pd
import numpy as np

def question1(pattern):
    n_trees = 0
    for y, line in pattern.iteritems():
        if line[current_x] == '#':
            n_trees +=1
        # print(current_x, y, line, line[current_x] == '#')
        current_x = (current_x + 3) % len(line)
        # print(current_x, y)

    print(n_trees)


def question2(pattern, right, down):
    current_x = 0
    n_trees = 0
    for ix in np.arange(0, len(pattern), down):
        line = pattern.iloc[ix]
        if line[current_x] == '#':
            n_trees +=1
        current_x = (current_x + right) % len(line)

    return n_trees


if __name__=='__main__':
    pattern = pd.read_csv('inputs/day03.txt', header=None)[0]
    
    a1 = question2(pattern, 1, 1)
    a2 = question2(pattern, 3, 1)
    a3 = question2(pattern, 5, 1)
    a4 = question2(pattern, 7, 1)
    a5 = question2(pattern, 1, 2)
    print(a1, a2, a3, a4, a5, a1*a2*a3*a4*a5)

