import re
import numpy as np

string_re = re.compile('"([a-z]+)"')
RULES = {}

def generate_group_rule(ix, group_rules, debug=False):
    if ix in RULES.keys():
        return RULES[ix]
    else:
        groups = group_rules[ix]
        new_group_rules = []
        for group in groups:
            new_rule = ['']
            for i in group:
                new = generate_group_rule(i, group_rules)
                if type(new[0])==list:
                    new_rule = [r+n for r in new_rule for n in n1 for n1 in new]
                else:
                    new_rule = [r+n for r in new_rule for n in new]

            new_group_rules += new_rule
        RULES[ix] = new_group_rules
        # print('Current rules:', RULES)
    return new_group_rules

def read_rules(rule_lines):
    group_rules = {}
    for line in rule_lines:
        ix, rule = line.split(':')
        match1 = string_re.search(rule)
        if match1:
            new_rule = match1.group(1)
            RULES[ix] = new_rule
        else:
            groups = [r.strip(' ').split(' ') for r in rule.split('|')]
            group_rules[ix] = groups
    return group_rules

def can_be_built(message, rules1, rules2):
    rules = [rules1, rules2]
    built_message = []
    l = 8

    # First add as many rules1 as possible
    i = 0
    n1, n2 = 0, 0
    is_valid = True    
    while i < len(message) and is_valid:
        is_valid = message[i:i+l] in rules1
        if is_valid:
            n1 += 1
            i += l

    # Then add as many rules2 as possible (starting from the end):
    j = len(message)
    is_valid = True
    while j>0 and is_valid:
        is_valid = message[j-l:j] in rules2
        if is_valid:
            n2 += 1
            j -= l

    # We need:
    # 1. n1 to be at least 2 (2 rules 42 added) ;
    # 2. j to be lower or equal to i (cover t the entire string) ;
    # 3. we cannot add more rules 31 than rules 42 so len(message - j) / 8 (number of rules 31) needs to be smaller than i / 8 (number of rules 42) + 1
    if n1 >= 2 and j <= i and n1-1 >= n2 and n2 > 0:
        return True
    else:
        return False 



if __name__=="__main__":

    with open('inputs/day19.txt', 'r') as handle:
        lines = handle.readlines()
        i = 0
        rule_lines = []
        while lines[i]!='\n':
            rule_lines.append(lines[i].strip('\n'))
            i+=1
        messages = [l.strip('\n') for l in lines[i+1:]]

    group_rules = read_rules(rule_lines)
    for ix in group_rules.keys():
        generate_group_rule(ix, group_rules)

    valid_messages = []
    invalid_messages = []
    for m in messages:
        if m in RULES['0']:
            valid_messages.append(m)
        else:
            invalid_messages.append(m)

    print('Valid:', len(valid_messages), 'Invalid:', len(invalid_messages))

    potential_valid = []
    for m in invalid_messages:
        if can_be_built(m, RULES['42'], RULES['31']):
            valid_messages.append(m)     

    print('Valid:', len(valid_messages))

