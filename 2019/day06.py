
def count_indirect_orbits(planet, orbits):
    center = orbits[planet]
    if center == 'COM':
        return 0
    else:
        return count_indirect_orbits(center, orbits) + 1

def find_path_to_com(planet, orbits):
    center = orbits[planet]
    if center == 'COM':
        return ['COM']
    else:
        return [center] + find_path_to_com(center, orbits) 

def question1(lines):
    direct_orbits = {}
    for l in lines:
        p1, p2 = l.strip('\n').split(')')
        direct_orbits[p2] = p1

    c = len(direct_orbits.keys())
    for planet in direct_orbits.keys():
        c += count_indirect_orbits(planet, direct_orbits)

    print(c)   

def find_first_path_intersection(shorter_path, longer_path):
    for i, planet in enumerate(longer_path):
        if planet in shorter_path:
            j = shorter_path.index(planet)
            return planet, i, j

if __name__=='__main__':
    with open('inputs/day06.txt', 'r') as handle:
        lines = handle.readlines()

    direct_orbits = {}
    for l in lines:
        p1, p2 = l.strip('\n').split(')')
        direct_orbits[p2] = p1

    my_path = find_path_to_com('YOU', direct_orbits)
    santa_path = find_path_to_com('SAN', direct_orbits)
    # print(my_path)
    # print(santa_path)
    longer_path = my_path if len(my_path)>len(santa_path) else santa_path
    shorter_path = my_path if len(my_path)<=len(santa_path) else santa_path
    planet, long_index, short_index = find_first_path_intersection(shorter_path, longer_path)
    print(long_index+short_index)