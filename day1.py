#!/usr/local/bin/python3
import InputHelper as IH

def solve1(input):
    return sum(convert(input, False))

def solve2(input):
    return sum(convert(input, True))

def convert(lines, recurse):
    return [calcModule(int(line), recurse) for line in lines]

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def calcModule(weight, recurse = False):
    our_weight = int(truncate(weight/3)) - 2

    #print(our_weight)

    if recurse:
        if our_weight <= 0:
            return 0
        else:
            return our_weight + calcModule(our_weight, True)
    else:
        return our_weight

data = IH.InputHelper(1).readlines()

print('Part 1 ', solve1(data))
print('2 ', calcModule(12))
print('2 ', calcModule(14))
print('654 ', calcModule(1969))
print('33583 ', calcModule(100756))

print('Part 2 ', solve2(data))
#print('2 ', calcModule(12, True))
print('966 ', calcModule(1969, True))
print('50346 ', calcModule(100756, True))