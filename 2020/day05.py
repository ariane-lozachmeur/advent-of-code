N_ROWS = 127
N_COLS = 7

def find_col_row(string, pos_type):
    start = 0
    if pos_type=='ROW':
        end = N_ROWS
    elif pos_type=='COL':
        end = N_COLS
    for char in string:
        if char=='F' or char == 'L':
            middle = int(start + ((end - start + 1) / 2))
            end = middle
        elif char=='B' or char == 'R':
            middle = int(start + ((end - start + 1) / 2))
            start = middle
    return start


def get_pos(string):
    row = find_col_row(string[:7], 'ROW')
    col = find_col_row(string[7:], 'COL')
    return row, col


def get_id(string):
    row, col = get_pos(string)
    return row * 8 + col

def run_test():
    s1 = 'FBFBBFFRLR'
    s2 = 'BFFFBBFRRR'
    s3 = 'FFFBBBFRRR'
    s4 = 'BBFFBBFRLL'
    
    assert get_id(s1) == 357
    assert get_id(s2) == 567
    assert get_id(s3) == 119
    assert get_id(s4) == 820


def find_max(input_file):
    max_id = 0
    with open(input_file, 'r') as handle:
        for l in handle.readlines():
            string = l.strip('\n')
            i = get_id(string)
            if i > max_id:
                max_id = i
        return max_id


def find_min_max(input_file):
    max_id = 0
    min_id = 1000
    ids = []
    with open(input_file, 'r') as handle:
        for l in handle.readlines():
            string = l.strip('\n')
            i = get_id(string)
            ids.append(i) 
            if i > max_id:
                max_id = i
            if i < min_id:
                min_id = i
        return min_id, max_id, sorted(ids)

def find_my_position(min_id, max_id, ids):
    current_candidate = None
    candidate_ids = []
    for i in range(len(ids)):
        this_id = ids[i]
        if min_id < this_id < max_id:
            if this_id > ids[i-1] + 1:
                print(ids[i-1] + 1)
            if this_id < ids[i+1] - 1:
                print(ids[i+1] - 1)

            
    return candidate_ids




if __name__=='__main__':
    min_id, max_id, ids = find_min_max('inputs/day05.txt')
    candidate_ids = find_my_position(min_id, max_id, ids)
