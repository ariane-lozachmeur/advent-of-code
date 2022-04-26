from intcode import *
from itertools import permutations 

def question1():
    max_output = 0
    best_perm = None
    
    for p in permutations('01234'):
        prev_output = '0'
        for i in range(5):
            program = program_str.split(',')

            phase_input = p[i]
            inputs = [prev_output, phase_input]

            _, prev_output = run_code(program, inputs)
            if prev_output > max_output:
                max_output = prev_output
                best_perm = p

    print('Max output', max_output)
    print('Best perm', best_perm)

def run_permutation(program_str, perm):
    programs = {i: program_str.split(',') for i in range(5)}
    positions = {i:0 for i in range(5)}
    stops = {i:False for i in range(5)}
    inputs = {i: [perm[i]] for i in range(5)}
    inputs[0] = [0] + inputs[0]
    
    while False in stops.values():
        for i in range(5):
            if i != 4:
                next_i = i+1
            else:
                next_i = 0
            
            step_output = None
            while step_output is None:  
                if stops[i]:
                    print('Final output for amp {} is: {}'.format(i, inputs[i]))
                    step_output = inputs[i][0]
                else:
                    programs[i], stops[i], step_output, incr = execute_step(programs[i], positions[i], inputs[i])
                    if step_output is not None:
                        print('Amp {} has an ouptut: {}'.format(i, step_output))
                        # print(programs[i], positions[i])
                        inputs[next_i] = [step_output] + inputs[next_i]
                        
                    positions[i] += incr

            if stops[i]:
                return inputs[0][0]
    # return inputs




if __name__=='__main__':

    with open('inputs/day07.txt') as handle:
        program_str = handle.readlines()[0].strip('\n')

    max_output = 0
    best_perm = None

    for perm in permutations('56789'):
        output = run_permutation(program_str, perm)
        if output > max_output:
            max_output = output
            best_perm = perm

    print(max_output)
    print(best_perm)


