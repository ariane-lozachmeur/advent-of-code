
def is_valid(password):
    has_double = False
    is_increment = True
    password_list = str(password)
    for i in range(1, len(password_list)):
        if password_list[i-1]==password_list[i]:
            has_double =  True
        if password_list[i-1]>password_list[i]:
            is_increment = False
    return is_increment and has_double

def is_valid_v2(password):
    has_double = False
    is_increment = True
    password_list = str(password)
    for i in range(1, len(password_list)):
        if password_list[i-1]==password_list[i]:
            # Look on the left and right side if the number are the same
            if ((i-2<0) or password_list[i-2] != password_list[i]) and ((i+1>=6) or password_list[i+1] != password_list[i]):
                has_double =  True
        if password_list[i-1]>password_list[i]:
            is_increment = False
    return is_increment and has_double


# def find_update_index(password):
#     for i in range(1, len(password)):
#         if password[i-1]>password[i]:
#             return i
#     return None

# def fix_increasing(password):
#     index = find_update_index(password)
#     while index is not None:
#         password[index:index+1] = password[index-1]
#         index = find_update_index(password)
#     return password

# def increment(password):
#     for pos in range(6):
#         if password[5-pos] != '9':
#             password[5-pos] = str(int(password[5-pos]) + 1)
#             return fix_increasing(password)



if __name__=='__main__':

    # print(is_valid_v2(123444))
    # print(is_valid_v2(111122))
    pmin = 234208
    pmax = 765869
    n = 0
    new = pmin
    while new <= pmax:
        n += is_valid_v2(new)
        new += 1

    print(n)
        


