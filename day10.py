#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math


def solve1(input):
    count = 0
    for value in range(input[0], input[1] + 1):
        if is_valid(value):
            count += 1
    
    return count

def solve2(input):
    count = 0
    for value in range(input[0], input[1] + 1):
        if is_valid_2(value):
            count += 1
    
    return count


def points_along_line(start, end):
    len_x = end[0] - start[0]
    len_y = end[1] - start[1]

    print(f'{len_x} {len_y}')
    print(math.gcd(len_x, len_y))

    gcd = math.gcd(len_x, len_y)
    vector = (int(len_x / gcd), int(len_y / gcd))
    print(vector)

    point = (start[0] + vector[0], start[1] + vector[1])
    print(point)

    while point[0] != end[0] or point[1] != end[1]:
        yield point
        point = (point[0] + vector[0], point[1] + vector[1])

#print('Part 1 ', solve1((264793, 803935)))
