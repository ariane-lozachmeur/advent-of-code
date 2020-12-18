import re

mem_regex = re.compile('mem\[([0-9]+)\] = ([0-9]+)')

def read_mask_q1(string_mask):
    mask_list = list(string_mask)
    return {i:m for i, m in enumerate(mask_list) if m!='X'}

def read_mask_q2(string_mask):
    return list(string_mask)

def get_bin(value, n_bits=36):
    bin1 = str(bin(value)[2:])
    return '0'*(n_bits-len(bin1))+bin1

def apply_mask_q1(value, mask_list):
    for pos, new_value in enumerate(mask_list):
        value = value[:pos] + new_value + value[pos+1:]
    return value

def apply_mask_q2(value, mask_list):
    values = [value]
    for pos, mask_value in enumerate(mask_list):
        # Overwrite the bit position by one in all possible values
        if mask_value == '1':
            for i in range(len(values)):
                values[i] = values[i][:pos] + '1' + values[i][pos+1:]
        # Overwrite the bit position by 0 in the value currently in the list 
        # and add another one with a 1 at that position
        elif mask_value == 'X':
            for i in range(len(values)):
                values[i] = values[i][:pos] + '0' + values[i][pos+1:]
                values.append(values[i][:pos] + '1' + values[i][pos+1:])
    return values

def question1():
    input_file = 'inputs/day14.txt'
    with open(input_file, 'r') as handle:
        lines = handle.readlines()

    memory = {}
    for l in lines:
        l = l.strip('\n') 
        if l.startswith('mask'):
            mask_dict = read_mask_q1(l.split(' = ')[-1])
            print(mask_dict)

        elif l.startswith('mem'):
            match = mem_regex.search(l)
            pos = int(match.group(1))
            value = int(match.group(2))
            value_bin = get_bin(value) 
            # print(value_bin)
            new_value_bin = apply_mask_q1(value_bin, mask_dict)
            # print(new_value_bin)
            new_value = int(new_value_bin, base=2)
            # print(new_value)
            memory[pos] = new_value

    print(memory)
    s = 0
    for value in memory.values():  
        s+=value
    print(s)

if __name__=='__main__':
    input_file = 'inputs/day14.txt'
    with open(input_file, 'r') as handle:
        lines = handle.readlines()

    memory = {}
    for l in lines:
        l = l.strip('\n') 
        if l.startswith('mask'):
            mask_list = read_mask_q2(l.split(' = ')[-1])

        elif l.startswith('mem'):
            match = mem_regex.search(l)
            pos = int(match.group(1))
            value = int(match.group(2))
            print(l, value)
            pos_bin = get_bin(pos) 
            # print(value_bin)
            all_pos_bin = apply_mask_q2(pos_bin, mask_list)
            # print(new_value_bin)
            for p_bin in all_pos_bin:
                memory[int(p_bin, base=2)] = value

    print(memory)
    s = 0
    for value in memory.values():  
        s+=value
    print(s)