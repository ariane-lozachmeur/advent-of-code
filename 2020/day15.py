from time import time

if __name__=='__main__':
    input_number_list = '11,18,0,20,1,7,16'.split(',')
    pos_dict = {int(n):int(i)+1 for i, n in enumerate(input_number_list)}
    current_pos = len(pos_dict) + 1
    prev_number = input_number_list[-1]
    while current_pos < 30000001:
        # start = time()
        new_number = (current_pos - 1) - pos_dict.get(prev_number, (current_pos - 1))
        pos_dict[prev_number] = (current_pos - 1)
        # end = time()
        # print('Time pos', current_pos, end-start)
        # print('Position', current_pos, 'previous number', prev_number, 'new number', new_number)
        # print(pos_dict)
        prev_number = new_number
        current_pos += 1
    print('Position', current_pos-1, 'previous number', prev_number, 'new number', new_number)
