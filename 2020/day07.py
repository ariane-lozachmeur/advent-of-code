import re
import numpy as np

container_regex = '^([a-z]+ [a-z]+) bag'
contained_regex = '(\d+) ([a-z\ ]*) bag'

def read_rules_v1(input_file):
    bag_rules = {}
    with open(input_file, 'r') as handle:
        for line in handle.readlines():
            m1 = re.match(container_regex, line)
            m2 = re.findall(contained_regex, line)
            bag_rules[m1.group(1)] = [bag for _, bag in m2]
    return bag_rules

def read_rules_v2(input_file):
    bag_rules = {}
    with open(input_file, 'r') as handle:
        for line in handle.readlines():
            m1 = re.match(container_regex, line)
            m2 = re.findall(contained_regex, line)
            bag_rules[m1.group(1)] = [(int(n), bag) for n, bag in m2]
    return bag_rules

def find_bag_can_contain(target, rules, explored=[]):
    print('Finding bags that can contain {}'.format(target))
    l = []

    for container, bag_list in rules.items():
        # if container in explored:
            # return l

        if target in bag_list:
            l.append(container)
            l += find_bag_can_contain(container, rules)#, explored=explored)
            explored.append(container)

    print(l)
    return l

def count_bags(target, rules):
    total = 0
    for n, bag in rules[target]:
        total += n
        total += n*count_bags(bag, rules)
    return total

def question1():
    target = 'shiny gold'
    rules = read_rules_v1('inputs/day07.txt')
    # print(rules)
    l = find_bag_can_contain(target, rules)
    print(len(np.unique(l)))

def question2():
    target = 'shiny gold'
    rules = read_rules_v2('inputs/day07.txt')
    total = count_bags(target, rules)
    print(total)


if __name__ == '__main__':
    target = 'shiny gold'
    rules = read_rules_v2('inputs/day07.txt')
    # print(rules)
    l = count_bags(target, rules)
    print(l)
