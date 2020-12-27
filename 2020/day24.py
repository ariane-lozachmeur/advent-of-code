import pandas as pd

def find_tile_index(line):
    x = 0
    y = 0
    i = 0
    while i < len(line):
        direction = line[i]
        if direction in ['n', 's']:
            direction += line[i+1]
            i+=2
            if direction == 'ne':
                y+=-1
            elif direction == 'nw':
                y+=-1
                x+=-1
            elif direction == 'sw':
                y+=1
            elif direction == 'se':
                y+=1
                x+=1
        elif direction == 'e':
            x+=1
            i+=1
        elif direction == 'w':
            x-=1
            i+=1
    return x, y


def count_black_tiles(grid):
    count = 0
    for y, row in grid.items():
        for x, tile in row.items():
            count += tile

    return count

def fill_up_grid(grid):
    ymin = min(list(grid.keys()))
    ymax = max(grid.keys())
    xmin = min([min(list(grid.get(y, {}).keys())) for y in range(ymin, ymax)])
    xmax = max([max(list(grid.get(y, {}).keys())) for y in range(ymin, ymax)])
    for y in range(ymin-2, ymax+2):
        if y not in grid.keys():
            grid[y] = {}
        for x in range(xmin-2, xmax+2):
            if x not in grid[y].keys():
                grid[y][x] = False
    return grid

def get_neigbors(x, y, grid):
    return [
        grid.get(y-1, {}).get(x-1, False),
        grid.get(y-1, {}).get(x, False),
        grid.get(y, {}).get(x+1, False),
        grid.get(y, {}).get(x-1, False),
        grid.get(y+1, {}).get(x, False),
        grid.get(y+1, {}).get(x+1, False)
        ]

def run_round(grid):
    '''
    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    '''
    ix_to_flip = []
    for y in grid.keys():
        for x in grid[y].keys():
            ns = get_neigbors(x, y, grid)
            count = ns.count(True)
            if grid[y][x] == False and count==2:
                ix_to_flip.append((x, y))
            elif grid[y][x] == True and (count==0 or count>2):
                ix_to_flip.append((x, y))
    for x, y in ix_to_flip:
        grid[y][x] = not grid[y][x]
    return fill_up_grid(grid)

def set_up_tiles(lines):
    grid = {}
    grid[0] = {}
    grid[0][0] = False # False is white, True is black
    instructions = {}
    for l in lines:
        x, y = find_tile_index(l)
        if y not in grid.keys():
            grid[y] = {}
        grid[y][x] = not grid[y].get(x, False)
    grid = fill_up_grid(grid)
    return grid


if __name__=="__main__":
    N = 100
    with open('inputs/day24.txt', 'r') as handle:
        lines = handle.readlines()
        lines = [l.strip('\n') for l in lines]

    grid = set_up_tiles(lines)
    print('Day 0: {}'.format(count_black_tiles(grid)))
    # print(pd.DataFrame(grid))

    for n in range(N):
        grid = run_round(grid)
        # print(pd.DataFrame(grid))
        # input('Continue?')
        print('Day {}: {}'.format(n+1, count_black_tiles(grid)))


