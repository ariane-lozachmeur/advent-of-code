import re
import pandas as pd

def has_fields(passport, fields):
    passport_fields = list(passport.keys())
    for nf in fields:
        if nf not in passport_fields:
            return False, nf
    return True, None

def byr_valid(byr):
    try:
        n_byr = int(byr)
    except:
        return False
    return len(byr)==4 and 1920 <= n_byr <= 2002

def iyr_valid(iyr):
    try:
        n_iyr = int(iyr)
    except:
        return False
    return len(iyr)==4 and 2010 <= n_iyr <= 2020 

def eyr_valid(eyr):
    try:
        n_eyr = int(eyr)
    except:
        return False
    return len(eyr)==4 and 2020 <= n_eyr <= 2030 

def hgt_valid(hgt):
    height_re = '([0-9]*)(cm|in)'    
    height_match = re.match(height_re, hgt)
    if not height_match:
        return False
    else:
        units = height_match.groups()[1]
        value = int(height_match.groups()[0])
        if units == 'in':
            return 59 <= value <= 76
        elif units == 'cm':
            return 150 <= value <= 193
        

def hcl_valid(hlc):
    eye_re = '^#[0-9a-f]{6}'
    if not re.match(eye_re, hlc):
        return False
    else:
        return True

def ecl_valid(ecl):
    return ecl in 'amb blu brn gry grn hzl oth'.split(' ')

def pid_valid(pid):
    try:
        n_pid = int(pid)
    except:
        return False
    return len(pid)==9

def read_passports(file):
    file1 = open(input_file, 'r') 
    passports = []
    line = file1.readline()
    while True:
        if not line:
            break
        current_passport = {}
        while line != '\n':
            if not line:
                break
            fields = line.replace('\n', '').split(' ')
            for f in fields:
                if ':' in f:
                    key, value = f.split(':')
                    current_passport[key] = value

            line = file1.readline()

        line = file1.readline()
        passports.append(current_passport)

    file1.close()
    return pd.DataFrame(passports)


if __name__=='__main__':

    input_file = 'inputs/day04.txt'
    necessary_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    passports = read_passports(input_file)
    passports['missing_fields'] = passports[necessary_fields].isna().sum(axis=1)

    valid_passports = passports[passports.missing_fields==0].copy()
    for f in necessary_fields:
        function = eval(f'{f}_valid')
        valid_passports['valid_{}'.format(f)] = valid_passports[f].apply(function)

    print(valid_passports.head())
    print(len(valid_passports[
        (valid_passports.valid_byr)&
        (valid_passports.valid_iyr)&
        (valid_passports.valid_eyr)&
        (valid_passports.valid_hgt)&
        (valid_passports.valid_hcl)&
        (valid_passports.valid_ecl)&
        (valid_passports.valid_pid)
        ]))
