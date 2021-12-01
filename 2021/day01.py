def count_incr(input_file):
    c = 0
    prev = 1000000000
    for l in open(input_file).readlines():
        if int(l)>prev:
            c+=1
        prev = int(l)

    return c

def sum(l):
    s = 0
    for i in l:
        s+=i
    return s

def count_incr_sliding(input_file):
    c = 0
    window = []
    for l in open(input_file).readlines():
        if len(window)==3:
            new_window = window[1:]+[int(l)]            
            if sum(new_window) > sum(window):
                c+=1

            window = new_window
        else:
            window.append(int(l))
        # print(window)
        # input('Continue?')

    return c

if __name__=='__main__':
    c = count_incr_sliding('inputs/day01.txt')
    print(c)