'''Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.'''


class Ship():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.head = (1, 0)
        self.waypoint = (10, -1)

    def __repr__(self):
        return "x: {} | y: {} | waypoint: {}".format(self.x, self.y, self.waypoint)

    def move_q1(self, direction, distance):
        if direction == 'N':
            self.y -= distance
        elif direction == 'S':
            self.y += distance
        elif direction == 'E':
            self.x += distance
        elif direction == 'W':
            self.x -= distance
        elif direction == 'F':
            self.x += distance * self.head[0]
            self.y += distance * self.head[1]

    def rotate_q1(self, direction, angle):
        if direction == 'L':
            angle = 360 - angle

        if angle == 90:
            self.head = (-self.head[1], self.head[0])
        elif angle == 180:
            self.head = (-self.head[0], -self.head[1])
        elif angle == 270:
            self.head = (self.head[1], -self.head[0])
        else:
            print("Error angle of {}".format(angle))
            raise SystemExit(1)     

    def move_waypoint(self, direction, distance):
        if direction == 'N':
            self.waypoint = (self.waypoint[0], self.waypoint[1] - distance)
        elif direction == 'S':
            self.waypoint = (self.waypoint[0], self.waypoint[1] + distance)
        elif direction == 'E':
            self.waypoint = (self.waypoint[0] + distance, self.waypoint[1])
        elif direction == 'W':
            self.waypoint = (self.waypoint[0] - distance, self.waypoint[1])

    def rotate_waypoint(self, direction, angle):
        if direction == 'L':
            angle = 360 - angle

        if angle == 90:
            self.waypoint = (-self.waypoint[1], self.waypoint[0])
        elif angle == 180:
            self.waypoint = (-self.waypoint[0], -self.waypoint[1])
        elif angle == 270:
            self.waypoint = (self.waypoint[1], -self.waypoint[0])
        else:
            print("Error angle of {}".format(angle))
            raise SystemExit(1)   

    def move(self, n):
        self.x += self.waypoint[0] * n
        self.y += self.waypoint[1] * n
   

    def get_distance(self):
        return abs(self.x) + abs(self.y)

def question1():
    input_file = 'inputs/day12.txt'
    with open(input_file, 'r') as handle:
        lines = handle.readlines()

    ship = Ship()
    for l in lines:
        direction = l[0]
        value = int(l.strip('\n')[1:])
        if direction in ['L', 'R']:
            ship.rotate_q1(direction, value)
        else:
            ship.move_q1(direction, value)
        
    print(ship.get_distance())  
      

if __name__=='__main__':
    input_file = 'inputs/day12.txt'
    with open(input_file, 'r') as handle:
        lines = handle.readlines()

    ship = Ship()
    for l in lines:
        direction = l[0]
        value = int(l.strip('\n')[1:])
        if direction in ['L', 'R']:
            ship.rotate_waypoint(direction, value)
        elif direction == 'F':
            ship.move(value)
        else:
            ship.move_waypoint(direction, value)
        
    print(ship.get_distance())






