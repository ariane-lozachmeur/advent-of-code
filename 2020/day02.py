import pandas as pd
import numpy as np

def is_valid_v1(password, letter, range):
    m, M = range.split('-')
    N = password.count(letter)
    return int(m) <= N <= int(M)

def is_valid_v2(password, letter, range):
    i1, i2 = range.split('-')
    p1 = int(i1)-1
    p2 = int(i2)-1

    if p2 < len(password):
        v2 = password[p2] == letter
    else:
        v2 = False
    if p1 < len(password):
        v1 = password[p1] == letter
    else:
        v2 = False

    if (v1 and v2) or (not v1 and not v2):
        return False
    else:
        return True



passwords = pd.read_csv('inputs/day02.txt', header=None, sep=' ')
passwords.columns = ['range', 'letter', 'password']

passwords.letter = passwords.letter.apply(lambda x: x.replace(':', ''))
passwords['is_valid'] = passwords.apply(lambda row: is_valid_v2(row.password, row.letter, row.range), axis=1)
print(passwords.head(10))
print(passwords.is_valid.value_counts())

