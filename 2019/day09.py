import intcode


if __name__=='__main__':
    instruction_str = open('inputs/day09.txt', 'r').readline()
    instructions = {i:value for i, value in enumerate(instruction_str.split(','))}

    code_list, all_outputs = intcode.run_code(instructions, ['2'])
    print(all_outputs)