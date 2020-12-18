op_n_parameters = {
    1:3,
    2:3,
    3:1,
    4:1,
    5:2,
    6:2,
    7:3,
    8:3,
    99:0
}


def read_opcode(opcode):
    instr_code = int(opcode[-2:])
    n_params = op_n_parameters[instr_code]
    # How many 0s do when need to add?
    padding = '0' * (n_params  - (len(opcode) - 2))
    mode_codes = padding + opcode[:-2]
    param_modes = []
    for i in range(n_params):
        param_modes.append(mode_codes[-(i+1)])
    return instr_code, param_modes

def get_values(code_list, modes, pos):
    values = []
    for i, m in enumerate(modes):
        param_pos = int(code_list[pos+i+1])
        if m == '0':
            values.append(int(code_list[param_pos]))
        elif m == '1':
            values.append(int(param_pos))
    return values


def execute_step(intcode, pos, this_input=None):
    this_output = None
    code_list = intcode.split(',')
    opcode = code_list[pos]
    instr_code, param_modes = read_opcode(opcode)
    params_values = get_values(code_list, param_modes, pos)
    # print(param_modes, params_values, code_list)
    incr = op_n_parameters[instr_code] + 1
    print('opcode: {} | params: {}'.format(opcode, params_values))
    print('before', code_list)
    if instr_code==99:
        return intcode, True, this_input, incr
    elif instr_code==1:
        v1 , v2, _ = params_values
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(v1 + v2)
    elif instr_code==2:
        v1, v2, _ = params_values
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(v1 * v2)
    elif instr_code==3:
        pos1 = int(code_list[pos+1])
        code_list[pos1] = this_input
    elif instr_code==4:
        this_output = params_values[0]
    elif instr_code==5:
        v1, v2 = params_values 
        if v1 != 0:
            # code_list[pos] = str(v2)
            # increment so that the new position is v2
            incr = v2 - pos
    elif instr_code==6:
        v1, v2 = params_values
        if v1 == 0:
            # code_list[pos] = str(v2)
            # increment so that the new position is v2
            incr = v2 - pos

    elif instr_code==7:
        v1, v2, _ = params_values
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(int(v1 < v2))
    elif instr_code==8:
        v1, v2, _ = params_values
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(int(v1 == v2))     
    else:
        raise UserException(code_list[pos], pos)

    print('after', code_list)
    print('new pos', pos+incr)
    return ','.join(code_list), False, this_output, incr

def run_code(intcode, code_input=None):
    pos = 0
    stop = False
    step_ouptput = code_input
    all_outputs = []
    while pos < len(intcode) and not stop:
        intcode, stop, step_ouptput, incr = execute_step(intcode, pos, step_ouptput)
        if step_ouptput is not None:
            all_outputs.append(step_ouptput)
        pos += incr

    return intcode, all_outputs


if __name__=='__main__':
    my_input = input('Enter input:')
    with open('inputs/day05.txt', 'r') as handle:
        code = handle.readline().strip('\n')
    print(run_code(code, my_input))


