op_n_parameters = {
    1:3,
    2:3,
    3:1,
    4:1,
    5:2,
    6:2,
    7:3,
    8:3,
    9:1,
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

def get_values(code_dict, modes, pos, relative_base):
    values = []
    for i, m in enumerate(modes):
        param_pos = int(code_dict[pos+i+1])
        if m == '0':
            values.append(int(code_dict.get(param_pos, 0)))
        elif m == '1':
            values.append(int(param_pos))
        elif m == '2':
            values.append(int(code_dict.get(param_pos+relative_base, 0)))
    return values, modes


def execute_step(code_dict, pos, code_inputs, relative_base):
    this_output = None
    opcode = code_dict.get(pos, 0)
    instr_code, param_modes = read_opcode(opcode)
    params_values, params_modes = get_values(code_dict, param_modes, pos, relative_base)
    incr = op_n_parameters[instr_code] + 1
    if instr_code==99:
        return code_dict, True, this_output, incr, relative_base
    elif instr_code==1:
        v1 , v2, _ = params_values
        pos3 = int(code_dict.get(pos+3, 0))
        if param_modes[2] == '2':
            pos3 += relative_base
        code_dict[pos3] = str(v1 + v2)
    elif instr_code==2:
        v1, v2, _ = params_values
        pos3 = int(code_dict.get(pos+3, 0))
        if param_modes[2] == '2':
            pos3 += relative_base

        code_dict[pos3] = str(v1 * v2)
    elif instr_code==3:
        pos1 = int(code_dict.get(pos+1, 0))
        if param_modes[0] == '2':
            pos1 += relative_base
        new_input = code_inputs.pop()
        code_dict[pos1] = new_input

    elif instr_code==4:
        this_output = params_values[0]
    elif instr_code==5:
        v1, v2 = params_values 
        if v1 != 0:
            # increment so that the new position is v2
            incr = v2 - pos

    elif instr_code==6:
        v1, v2 = params_values
        if v1 == 0:
            # increment so that the new position is v2
            incr = v2 - pos

    elif instr_code==7:
        v1, v2, pos3 = params_values
        pos3 = int(code_dict.get(pos+3, 0))
        if param_modes[2] == '2':
            pos3 += relative_base
        code_dict[pos3] = str(int(v1 < v2))
    elif instr_code==8:
        v1, v2, _ = params_values
        pos3 = int(code_dict.get(pos+3, 0))
        if param_modes[2] == '2':
            pos3 += relative_base
        code_dict[pos3] = str(int(v1 == v2))   
    elif instr_code == 9:
        # Opcode 9 adjusts the relative base by the value of its only parameter. 
        # The relative base increases (or decreases, if the value is negative)
        # by the value of the parameter.
        v1 = params_values[0]
        relative_base += v1
    else:
        raise UserException(code_dict[pos], pos)

    # print('After', code_dict)
    return code_dict, False, this_output, incr, relative_base

def run_code(code_dict, code_inputs):
    pos = 0
    stop = False
    relative_base = 0
    all_outputs = []
    while pos < len(code_dict) and not stop:
        code_dict, stop, step_output, incr, relative_base = execute_step(code_dict, pos, code_inputs, relative_base)
        if step_output is not None:
            code_inputs.append(step_output)
            all_outputs.append(step_output)
        pos += incr

    return code_dict, all_outputs

