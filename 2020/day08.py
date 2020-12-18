from copy import copy

def execute_line(pos, cumul, lines, debug=False):
    op, arg = lines[pos].strip('\n').split(' ')
    sign = arg[0]
    arg_int = int(arg[1:]) if sign == '+' else -int(arg[1:])
    if op == 'acc':
        cumul += arg_int
        pos += 1

    elif op == 'jmp':
        pos += arg_int

    elif op == 'nop':
        pos += 1
    
    if debug:
        print(op, arg_int, cumul)

    return pos, cumul

def generate_new_code(lines, last_update_pos):
    new_lines = copy(lines)

    for i in range(last_update_pos+1, len(new_lines)):
        if new_lines[i].startswith('nop'):
            new_lines[i] = new_lines[i].replace('nop', 'jmp')
            return i, new_lines
        elif new_lines[i].startswith('jmp'):
            new_lines[i] = new_lines[i].replace('jmp', 'nop')
            return i, new_lines

def run_program(lines, debug=False):
    cumul = 0
    visited = []
    pos = 0

    while pos not in visited and pos < len(lines):
        visited.append(pos)
        pos, cumul  = execute_line(pos, cumul, lines, debug)

    if pos in visited:
        print('Error, infinite loop')
        return False
    elif pos >= len(lines):
        print('Program ended with accumulator at {}'.format(cumul))
        return True

if __name__=='__main__':
    with open('inputs/day08.txt') as handle:
        lines = list(handle.readlines())

    last_update = 0
    is_valid = False
    while not is_valid and last_update < len(lines):
        last_update, new_lines = generate_new_code(lines, last_update)
        is_valid = run_program(new_lines)

    if is_valid:
        run_program(new_lines, debug=True)


    