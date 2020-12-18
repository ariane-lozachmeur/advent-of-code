

def get_subexpression(expression):
    parenthesis_counter = 1
    if not expression.startswith('('):
        print(expression)
         
    for i, char in enumerate(expression[1:]):
        if char=='(':
            parenthesis_counter += 1
        elif char==')':
            parenthesis_counter -= 1
        if parenthesis_counter == 0:
            return expression[1:i+1], i+2

def complex_math_q1(expression):
    expression_list = list(expression)
    total = 0
    current_op = '+'
    i = 0
    while i < len(expression_list):
        character = expression_list[i]
        if character == ' ':
            pass
        elif character in ['+', '*']:
            current_op = character
        elif character=='(':
            # Select the expression inside the parenthesis and compute the results of this one
            new_expr, incr = get_subexpression(expression[i:])
            print('New expression', new_expr)
            i+=incr
            print('Rest', expression[i+1:])
            new_value = complex_math(new_expr)
            if current_op == '+':
                total += new_value
            elif current_op == '*':
                total *= new_value
            else:
                print('Error no current op in {}'.format(expression))
        elif current_op=='+':
            total += int(character)
        elif current_op=='*':
            total *= int(character)
        else:
            print('Error no current op in {}'.format(expression))

        i+=1
    print(expression, total)
    return total

def simple_math_q2(expression):
    assert expression.count('(')==0 and expression.count(')') == 0
    if '+' in expression:
        i = expression.index('+')
        v1 = expression[:i].split(' ')[-2]
        v2 = expression[i+1:].split(' ')[1]
        v3 = str(int(v1) + int(v2))
        new_expr = expression[:i-len(v1)-1]+v3+expression[i+len(v2)+2:]
        print('Next (addition)', new_expr)
        return simple_math_q2(new_expr)
    elif '*' in expression:
        i = expression.index('*')
        v1 = expression[:i].split(' ')[-2]
        v2 = expression[i+1:].split(' ')[1]
        # print(int(v1) * int(v2))
        v3 = str(int(v1) * int(v2))
        new_expr = expression[:i-len(v1)-1]+v3+expression[i+len(v2)+2:]
        print('Next (multiplication)', new_expr)
        return simple_math_q2(new_expr)
    else:
        # print(expression)
        return expression

def complex_math_q2(expression):
    if '(' in expression:
        i = expression.index('(')
        subexpr, incr = get_subexpression(expression[i:])
        new_value = complex_math_q2(subexpr)
        new_expr = expression[:i]+new_value+expression[i+incr:]
        print('Next (parenthesis)', new_expr)
        return complex_math_q2(new_expr)
    else:
        print(expression)
        return simple_math_q2(expression)



    expression_list = list(expression)
    total = 0
    current_op = '+'
    i = 0
    while i < len(expression_list):
        character = expression_list[i]
        if character == ' ':
            pass
        elif character in ['+', '*']:
            current_op = character
        elif character=='(':
            # Select the expression inside the parenthesis and compute the results of this one
            new_expr, incr = get_subexpression(expression[i:])
            print('New expression', new_expr)
            i+=incr
            print('Rest', expression[i+1:])
            new_value = complex_math(new_expr)
            if current_op == '+':
                total += new_value
            elif current_op == '*':
                total *= new_value
            else:
                print('Error no current op in {}'.format(expression))
        elif current_op=='+':
            total += int(character)
        elif current_op=='*':
            total *= int(character)
        else:
            print('Error no current op in {}'.format(expression))

        i+=1
    print(expression, total)
    return total




i0, r01, r02= '1 + 2 * 3 + 4 * 5 + 6', 71, 231
i1, r11, r12 = '2 * 3 + (4 * 5)', 26, 46
i2, r21, r22 = '5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445
i3, r31, r32 = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',  12240, 669060
i4, r41, r42 = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2' ,  13632, 23340

if __name__=="__main__":
    with open('inputs/day18.txt', 'r') as handle:
        lines = handle.readlines()

    # print(complex_math_q2(i3))
    # print(str(int('21') * int('11')))

    total = 0
    for l in lines:
        print(l)
        total += int(complex_math_q2(l.strip('\n')))
    print(total)



