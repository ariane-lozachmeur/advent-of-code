from itertools import permutations  

def is_valid(number, sublist):
    p = permutations(sublist, 2)
    for n1, n2 in p:
        if n1+n2==number and n1!=n2:
            return True
    return False

def find_sum(target, sublist):
    cumul = 0
    i = 0
    while cumul < target and i<len(sublist):
        cumul+=sublist[i]
        i+=1
    if cumul==target:
        return sublist[:i]
    else:
        return None

def question1():
    window = 25
    current_pos = window
    with open('inputs/day09.txt') as handle:
        numbers = [int(l.strip('\n')) for l in handle.readlines()]

    for current_pos in range(window, len(numbers)):
        this_number = numbers[current_pos]
        sublist = numbers[current_pos-window:current_pos]
        if not is_valid(this_number, sublist):
            print(this_number)
            break


if __name__=='__main__':
    current_pos = 0
    target = 144381670
    with open('inputs/day09.txt') as handle:
        numbers = [int(l.strip('\n')) for l in handle.readlines()]

    for current_pos in range(len(numbers)):
        sublist = numbers[current_pos:]
        
        valid_sublist = find_sum(target, sublist)
        if valid_sublist is not None:
            print(valid_sublist)
            print(min(valid_sublist)+max(valid_sublist))
            break