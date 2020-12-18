

if __name__=='__main__':
    total = 0
    with open('inputs/day06.txt') as handle:
        line = handle.readline()
        groups = []
        while True:
            if not line:
                break
            current_passport = {}
            new_group = {}
            group_size = 0
            while line != '\n':
                if not line:
                    break

                group_size += 1
                for letter in line.strip('\n'):
                    if letter not in new_group.keys():
                        new_group[letter] = 1
                    else:
                        new_group[letter] += 1
                line = handle.readline()

            new_group_all = {k: v for k, v in new_group.items() if v==group_size}
            total += len(new_group_all.keys())
            groups.append(new_group_all)

            line = handle.readline()

    # print(groups)
    print(total)