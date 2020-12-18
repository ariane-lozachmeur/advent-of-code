
def input_to_table(input_file):
    table = []
    with open(input_file, 'r') as handle:
        for line in handle.readlines():
            new_row = list(line.strip('\n'))
            table.append(new_row)

    return table

def pad_table(table):
    # Pad the area with floor to avoid any issues with side effect
    # Pad to top and bottom
    table = [['.']*len(table[0])] + table + [['.']*len(table[0])]
    print(table)
    # Pad the sides
    table = [
        ['.'] + row + ['.'] for row in table
    ]
    return table

def count_occupied_seats_q1(pos, table):
    x, y = pos
    n = 0
    for x1, y1 in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
        # print(x1, y1)
        # print(table[y1])
        n += table[y1][x1] == '#'
    return n

def count_occupied_seats_q2(pos, table):
    x, y = pos
    n = 0
    # Upper left corner:
    seat = '.'
    i = 1
    while seat == '.' and (y-i)>0 and (x-i)>0:
        seat = table[y-i][x-i]
        i += 1

    n += seat == '#'

    # Upper seat:
    seat = '.'
    i = 1
    while seat == '.' and (y-i)>0:
        seat = table[y-i][x]
        i += 1
    n += seat == '#'    

    # Upper right corner
    seat = '.'
    i = 1
    while seat == '.' and (y-i)>0 and (x+i)<x_max:
        seat = table[y-i][x+i]
        i += 1
    n += seat == '#' 

    # Left seat
    seat = '.'
    i = 1
    while seat == '.' and (x-i)>0:
        seat = table[y][x-i]
        i += 1
    n += seat == '#' 

    # Right seat
    seat = '.'
    i = 1
    while seat == '.' and (x+i)<x_max:
        seat = table[y][x+i]
        i += 1
    n += seat == '#' 

    # Lower left corner:
    seat = '.'
    i = 1
    while seat == '.' and (y+i)<y_max and (x-i)>0:
        seat = table[y+i][x-i]
        i += 1
    n += seat == '#'

    # Lower seat:
    seat = '.'
    i = 1
    while seat == '.' and (y+i)<y_max:
        seat = table[y+i][x]
        i += 1
    n += seat == '#'    

    # Lower right corner
    seat = '.'
    i = 1
    while seat == '.' and (y+i)<y_max and (x+i)<x_max:
        seat = table[y+i][x+i]
        i += 1
    n += seat == '#' 

    return n


def update_table(table, max_occupied):
    new_table = []        
    for y in range(y_max):
        new_table_row = []
        for x in range(x_max):
            if table[y][x] == '.':
                new_table_row.append(table[y][x])
            else:
                n = count_occupied_seats_q2((x, y), table)
                if n == 0:
                    new_table_row.append('#')
                elif n > max_occupied:
                    new_table_row.append('L')
                else:
                    new_table_row.append(table[y][x])
        new_table.append(new_table_row)
    return new_table

def count_occupied(table):
    n = 0
    for row in table:
        n += row.count('#')
    return n


if __name__=='__main__':

    table = input_to_table('inputs/day11.txt')
    table = pad_table(table)
    # Don't forget those are the dimension with the padding
    x_max = len(table[0])
    y_max = len(table)

    # Round 1:
    new_table = update_table(table, 4)

    # Other rounds until table
    while new_table!=table:
        table = list(new_table)
        new_table = update_table(table, 4)

    print(count_occupied(table))