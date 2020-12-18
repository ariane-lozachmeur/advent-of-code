import re

rules_regex = re.compile('([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)')

def parse_input(input_file):
    rules = {}
    tickets = []
    with open(input_file, 'r') as handle:
        lines = handle.readlines()

    l = lines[0]
    i = 0
    while l != '\n':
        match = rules_regex.search(l.strip('\n'))
        field = match.group(1)
        low1 = match.group(2)
        high1 = match.group(3)
        low2 = match.group(4)
        high2 = match.group(5)
        rules[field] = [(int(low1), int(high1)), (int(low2), int(high2))]

        i += 1
        l = lines[i]

    # jump the new line
    i += 2
    l = lines[i].strip('\n')
    my_ticket = l.split(',')

    # jump the new line and the header
    i+=3
    l = lines[i]
    while i < len(lines):
        tickets.append(lines[i].strip('\n').split(','))
        i+=1

    return rules, my_ticket, tickets

def value_is_valid_q1(value, rules):
    for r, (i1, i2) in rules.items():
        if (i1[0] <= value <= i1[1]) or (i2[0] <= value <= i2[1]):
            return True
    return False

def is_valid_q1(ticket, rules):
    invalid_values = []
    for value in ticket:
        is_valid = value_is_valid_q1(int(value), rules)
        if not is_valid:
            invalid_values.append(int(value))
    return invalid_values

def question1():
    rules, my_ticket, tickets = parse_input('inputs/day16.txt')
    invalid_values = []
    for ticket in tickets:
        invalid_values += is_valid_q1(ticket, rules)

    print(sum(invalid_values))

def filter_tickets(tickets, rules):
    valid_tickets = []
    for ticket in tickets:
        if len(is_valid_q1(ticket, rules))==0:
            valid_tickets.append(ticket)
    return valid_tickets

def sort_out_fields(valid_tickets, rules):
    # At first, every field can potentially be for every rule
    potential_fields = {}
    for pos in range(len(valid_tickets[0])):
        valid_fields = list(rules.keys())
        i = 0
        while len(valid_fields)>1 and i<len(valid_tickets):
            for ticket in valid_tickets:
                i += 1
                for r in valid_fields:
                    value = int(ticket[pos])
                    i1, i2 = rules[r]
                    # If the value is not in the correct intervals, remove the field from the potential fields
                    if not ((i1[0] <= value <= i1[1]) or (i2[0] <= value <= i2[1])):
                        valid_fields.remove(r)

        potential_fields[pos] = valid_fields
    return potential_fields

def find_unique_fields(potential_fields, rules):
    non_attributed = list(rules.keys())
    attributions = {}
    while len(non_attributed)>0:
        for pos, fields in potential_fields.items():
            fields = [f for f in fields if f in non_attributed]
            potential_fields[pos] = fields
            if len(fields)==1:
                print('Position {} is {}'.format(pos, fields[0]))
                attributions[fields[0]] = pos
                non_attributed.remove(fields[0])

    return attributions




if __name__=='__main__':
    rules, my_ticket, tickets = parse_input('inputs/day16.txt')
    valid_tickets = filter_tickets(tickets, rules)
    potential_fields = sort_out_fields(valid_tickets, rules)
    unique_fields = find_unique_fields(potential_fields, rules)

    mult = 1
    for rule in rules.keys():
        if rule.startswith('departure'):
            pos = unique_fields[rule]
            mult *= int(my_ticket[pos])

    print(mult)





