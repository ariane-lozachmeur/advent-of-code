'''The Intcode program will serve as the brain of the robot. 
The program uses input instructions to access the robot's camera: 
provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. 
Then, the program will output two values:

First, it will output a value indicating the color to paint the panel the robot is over:
 0 means to paint the panel black, and 
 1 means to paint the panel white.
Second, it will output a value indicating the direction the robot should turn: 
0 means it should turn left 90 degrees, and 
1 means it should turn right 90 degrees.
After the robot turns, it should always move forward exactly one panel.
The robot starts facing up.

The robot will continue running 
for a while like this and halt when it is finished drawing. 
Do not restart the Intcode computer inside the robot during this process.'''

import intcode

if __name__=='__main__':
    program = open('inputs/day11.txt').readline().split(',')
    program = {i:instr for i, instr in enumerate(program)}

    inputs = ['1']
    robot_pos = (0, 0)
    robot_facing = (0, 1) # facing up
    grid = {0:{0:'#'}}
    
    intcode_pos = 0
    stop = False
    relative_base = 0
    current_outputs = []
    while not stop:
        program, stop, step_output, incr, relative_base = intcode.execute_step(program, intcode_pos, inputs, relative_base)
        if step_output is not None:
            current_outputs.append(step_output)

        # After 2 numbers have been outputed
        if len(current_outputs)==2:
            # add the row if necesary
            if robot_pos[1] not in grid.keys():
                    grid[robot_pos[1]] = {}
            # paint the appropriate color
            if current_outputs[0]==0:
                grid[robot_pos[1]][robot_pos[0]] = '.'
            else:
                grid[robot_pos[1]][robot_pos[0]] = '#'
            # rotate robot
            if current_outputs[1]==0:
                robot_facing = (robot_facing[1], -robot_facing[0])
            else:
                robot_facing = (-robot_facing[1], robot_facing[0])
            # move forward and reset inputs
            robot_pos = (robot_pos[0] + robot_facing[0], robot_pos[1] + robot_facing[1])
            # reset outputs and set new input
            current_outputs = []
            inputs = [int(grid.get(robot_pos[1], {}).get(robot_pos[0], '.') == '#')]

        intcode_pos += incr

    # print number of painted panels and get xmin and xmax
    c = 0
    xmin = 1000
    xmax = -1000
    for key1 in grid.keys():
        for key2 in grid[key1].keys():
            if key2 < xmin:
                xmin = key2
            if key2 > xmax:
                xmax = key2
            c+=1
    print(c)
    # print what is painted
    ys = sorted(grid.keys(), reverse=True)
    print(ys)
    print(xmin, xmax)
    for x in range(xmin, xmax):
        row = ''
        for y in ys:
            row += grid[y].get(x, '.').replace('.', '  ').replace('#', '##')
        print(row)

    # Prev guess AKFRJFHK, AKFRIFHK
