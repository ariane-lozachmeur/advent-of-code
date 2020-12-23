from copy import copy
import math

class Image():
    def __init__(self, dimension, tiles):
        self.tile_pos = [[None for _ in range(dimension)] for _ in range(dimension)]
        self.tiles = tiles
        self.corners = []
        self.sides = []
        self.placed_ids = []
        self.dimension = dimension
        self.width = dimension * 8

    def __str__(self):
        string = ''
        for i, row in enumerate(self.image):
            string += ''.join(row)+'\n'
        return string

    def place_tiles(self, first_corner):
        # Place and orient the first corner
        unmatched_sides = first_corner.get_unmatched_sides()
        if unmatched_sides == ['right', 'up']:
            first_corner.rotate_left(True)
        elif unmatched_sides == ['left', 'up']:
            first_corner.rotate_left(False)
            first_corner.rotate_left(True)
        elif unmatched_sides == ['left', 'low']:
            first_corner.rotate_left(False)
            first_corner.rotate_left(False)
            first_corner.rotate_left(True)
        self.tile_pos[0][0] = first_corner.id
        self.placed_ids.append(first_corner.id)

        # Place the first row
        for x in range(dim):
            current_tile_id = self.tile_pos[0][x]
            current_tile = self.tiles[current_tile_id]
            current_border = current_tile.borders['right']
            for neighbor_id in current_tile.neighbors:
                if neighbor_id not in self.placed_ids:
                    neighbor = self.tiles[neighbor_id]
                    match = orient_tile(neighbor, current_border, 'left')
                    if match is not None:
                        self.tile_pos[0][x+1] = neighbor_id
                        self.placed_ids.append(neighbor_id)

        # Place column by column
        for x in range(dim):
            for y in range(dim):
                current_tile_id = self.tile_pos[y][x]
                current_tile = self.tiles[current_tile_id]
                current_border = current_tile.borders['low']
                for neighbor_id in current_tile.neighbors:
                    if neighbor_id not in self.placed_ids:
                        neighbor = self.tiles[neighbor_id]
                        match = orient_tile(neighbor, current_border, 'up')
                        if match is not None:
                            self.tile_pos[y+1][x] = neighbor_id
                            self.placed_ids.append(neighbor_id)

    def assemble(self, add_gaps=False):
        self.image = []
        for row in self.tile_pos:
            new_rows = [[] for _ in range(8)]
            for tile_id in row:
                this_tile = self.tiles[tile_id]
                # Remove the edges
                for i, tile_row in enumerate(this_tile.image[1:-1]):
                    if add_gaps:
                        new_rows[i] += tile_row[1:-1] + [' ']
                    else:
                        new_rows[i] += tile_row[1:-1]

            if add_gaps:
                self.image += new_rows + [' ']
            else:
                self.image += new_rows

    def rotate_left(self):
        new_image = [['' for _ in range(self.width)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.width):
                new_image[self.width-1-x][y] = self.image[y][x]
        self.image = new_image

    def flip_x(self):
        new_image = [['' for _ in range(self.width)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.width):
                new_image[y][self.width-1-x] = self.image[y][x]
        self.image = new_image


    def pattern_match(self, pattern_index, window):
        x, y = window
        for l, indexes in enumerate(pattern_index):
            for i in indexes:
                if self.image[y+l][x+i] != '#':
                    return False
        return True

    def find_patterns(self, pattern_index):
        window_width = 20
        window_length = 3
        patterns_pos = []
        for x in range(self.width - window_width):
            for y in range(self.width - window_length):
                match = self.pattern_match(pattern_index, (x, y))
                if match:
                    patterns_pos.append((x, y))
        return patterns_pos

    def count_waves(self, number_of_monsters):
        # Each monster represent 15 fake waves, so we can simply remove that from the total.
        count = 0
        for row in self.image:
            count += row.count('#')
        return count - (number_of_monsters*15)

class Tile():
    def __init__(self, this_id):
        self.id = this_id
        self.image = []
        self.neighbors = []
        self.shared_borders = []

    def __str__(self):
        string = ''
        for i, row in enumerate(self.image):
            string += ''.join(row)+'\n'
        return string

    # def set_neigbors(self, neighbor_id, shared_border):
    #     self.

    def add_row(self, line):
        self.image.append(list(line))

    def rotate_left(self, reset_borders=True):
        new_image = [['' for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                new_image[9-x][y] = self.image[y][x]
        self.image = new_image
        if reset_borders:
            self.set_all_borders()

    def flip_x(self, reset_borders=True):
        new_image = [['' for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                new_image[y][9-x] = self.image[y][x]
        self.image = new_image
        if reset_borders:
            self.set_all_borders()

    def flip_y(self, reset_borders=True):
        new_image = [['' for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                new_image[9-y][x] = self.image[y][x]
        self.image = new_image
        if reset_borders:
            self.set_all_borders()

    def set_borders(self):
        borders = {}
        for i, label in enumerate(['up', 'right', 'low', 'left']):
            if label in ['up', 'right']:
                borders[label] = ''.join(self.image[0])
            elif label in ['low', 'left']:
                borders[label] = ''.join(self.image[0][::-1])
            self.rotate_left(reset_borders=False)
        self.rotate_left(reset_borders=False)
        return borders

    def set_all_borders(self):
        borders = self.set_borders()
        self.borders = borders
        self.flip_x(reset_borders=False)
        new_borders = self.set_borders()
        self.borders_r = new_borders
        self.flip_x(reset_borders=False)

    def get_all_borders(self):
        return list(self.borders.values()) + list(self.borders_r.values())

    def find_potential_neighbors(self, tiles):
        this_borders = self.get_all_borders()
        for i in tiles.keys():
            if i != self.id:
                intersection = [b for b in this_borders if b in (tiles[i].get_all_borders())]
                if len(intersection)>0:
                    self.neighbors.append(i)
                    self.shared_borders += intersection


    def get_unmatched_sides(self):
        unmatched_sides = []
        for label, border in self.borders.items():
            if border not in self.shared_borders:
                unmatched_sides.append(label)

        unmatched_sides = sorted(unmatched_sides)
        return unmatched_sides

        
def read_tiles(lines):
    tiles = {}
    for l in lines:
        if l.startswith('Tile'):
            current_id = l.split(' ')[1].strip(':')
            tiles[current_id] = {}
            new_tile = Tile(current_id)
        elif l=='':
            tiles[current_id]=new_tile
        else:
            new_tile.add_row(l)
    # add the last one
    tiles[current_id]=new_tile
    return tiles

def find_corners(tiles):
    corners = []
    product = 1
    for i in tiles.keys():
        tiles[i].find_potential_neighbors(tiles)
        if len(tiles[i].neighbors)==2:
            corners.append(tiles[i])

    return corners, product

def question1():
    with open('inputs/day20.txt', 'r') as handle:
        lines = handle.readlines()
        lines = [l.strip('\n') for l in lines]

    tiles = read_tiles(lines)
    for i in tiles.keys():
        tiles[i].set_all_borders()
    
    corners,_ , product = find_corners_and_sides(tiles)
    print(product)

def orient_tile(tile, border_to_match, position_to_match):
    for i in range(4):
        if tile.borders[position_to_match] == border_to_match:
            return tile
        else:
            tile.rotate_left(True)
    tile.flip_x(True)
    for i in range(4):
        if tile.borders[position_to_match] == border_to_match:
            return tile
        else:
            tile.rotate_left(True)    
    return None

if __name__=="__main__":
    pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    pattern_index = [
        [18],
        [0, 5, 6, 11, 12, 17, 18, 19],
        [1, 4, 7, 10, 13, 16]
    ]
    with open('inputs/day20.txt', 'r') as handle:
        lines = handle.readlines()
        lines = [l.strip('\n') for l in lines]

    tiles = read_tiles(lines)
    dim = int(math.sqrt(len(tiles)))
    image = Image(dim, tiles)

    borders = {}
    for i in tiles.keys():
        borders[i] = tiles[i].set_all_borders()
    
    image.corners, _ = find_corners(image.tiles)
    image.place_tiles(image.corners[0])
    image.assemble(False)

    # Find the correct orientation by rotating and flipping until we find at least one monster
    n_rotate = 0
    patterns = []
    while n_rotate < 4 and len(patterns)==0:
        patterns = image.find_patterns(pattern_index)
        image.rotate_left()
        n_rotate +=1

    if len(patterns) == 0:
        n_rotate = 0
        image.flip_x()
        while n_rotate < 4 and len(patterns)==0:
            patterns = image.find_patterns(pattern_index)
            image.rotate_left()
            n_rotate +=1

    print(len(patterns))
    roughness = image.count_waves(len(patterns))
    print(roughness)





