
def execute_step(intcode, pos):
    code_list = intcode.split(',')
    if code_list[pos]=='99':
        return intcode, True
    elif code_list[pos]=='1':
        pos1 = int(code_list[pos+1])
        pos2 = int(code_list[pos+2])
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(int(code_list[pos1]) + int(code_list[pos2]))
    elif code_list[pos]=='2':
        pos1 = int(code_list[pos+1])
        pos2 = int(code_list[pos+2])
        pos3 = int(code_list[pos+3])
        code_list[pos3] = str(int(code_list[pos1]) * int(code_list[pos2]))
    else:
        raise UserException(code_list[pos], pos)

    return ','.join(code_list), False

def run_code(intcode):
    pos = 0
    stop = False
    while pos < len(intcode) and not stop:
        intcode, stop = execute_step(intcode, pos)
        pos += 4

    return intcode

def run_tests():
    assert run_code('1,9,10,3,2,3,11,0,99,30,40,50') == '3500,9,10,70,2,3,11,0,99,30,40,50'
    assert run_code('1,0,0,0,99') == '2,0,0,0,99'
    assert run_code('2,3,0,3,99') == '2,3,0,6,99'
    assert run_code('2,4,4,5,99,0') == '2,4,4,5,99,9801'
    assert run_code('1,1,1,4,99,5,6,0,99') == '30,1,1,4,2,5,6,0,99'


def run_instructions(i1, i2):
    with open('inputs/day02.txt') as handle:
        og_intcode = handle.readline()
    
    intcode_list = og_intcode.split(',')
    intcode_list[1] = str(i1)
    intcode_list[2] = str(i2)
    intcode = ','.join(intcode_list)
    new_intcode = run_code(intcode)
    return int(new_intcode.split(',')[0])

def question1():
    print(run_instructions(12, 2))


def question2():
    target = 19690720
    for noun in range(0, 99):
        for verb in range(0, 99):
            if target == run_instructions(noun, verb):
                print(noun, verb, 100 * noun + verb)



if __name__ == '__main__':
    # To do this, before running the program, replace position 1 with the value 12 
    # and replace position 2 with the value 2. What value is left at position 0 after the program halts?
    question2()


