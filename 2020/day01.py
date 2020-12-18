import pandas as pd
import numpy as np


def find_two(numbers, target):
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            result = numbers[i]+numbers[j]
            if result == target:
                return numbers[i], numbers[j]

def find_three(numbers, target):
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            for k in range(j, len(numbers)):
                result = numbers[i]+numbers[j]+numbers[k]
                if result == target:
                    return numbers[i], numbers[j], numbers[k]



numbers = pd.read_csv('inputs/day01.txt', header=None)
numbers = numbers[0]
target = 2020

for i in range(len(numbers)):
    for j in range(i, len(numbers)):
        for k in range(j, len(numbers)):
            result = numbers[i]+numbers[j]+numbers[k]
            if result == target:
                print(numbers[i], numbers[j], numbers[k], numbers[i]*numbers[j]*numbers[k])
