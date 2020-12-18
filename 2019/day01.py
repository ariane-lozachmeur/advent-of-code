def compute_fuel(mass):
    return int(mass/3)-2

def compute_all_fuel_rec(mass):
    needed_fuel = compute_fuel(mass)
    total_fuel = 0
    while needed_fuel > 0:
        total_fuel += needed_fuel
        needed_fuel = compute_fuel(needed_fuel)

    return total_fuel

def run_tests1():
    assert (compute_fuel(12)==2)
    assert (compute_fuel(14)==2)
    assert (compute_fuel(1969)==654)
    assert (compute_fuel(100756)==33583)


def run_tests2():
    assert (compute_all_fuel_rec(14)==2)
    assert (compute_all_fuel_rec(1969)==966)
    assert (compute_all_fuel_rec(100756)==50346)



if __name__=='__main__':
    total = 0
    with open('inputs/day01.txt') as handle:
        for l in handle.readlines():
            total += compute_all_fuel_rec(int(l)) 
    print(total)