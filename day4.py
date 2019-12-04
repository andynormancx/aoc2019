#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections


def solve1(input):
    count = 0
    for value in range(input[0], input[1] + 1):
        if is_valid(value):
            count += 1
    
    return count


def is_valid(value):
    digits = [int(digit) for digit in str(value)]
    last_digit = 0
    two_the_same = False

    for digit in digits:
        if digit < last_digit:
            return False
        
        if digit == last_digit:
            two_the_same = True

        last_digit = digit

    return two_the_same

def solve2(input):
    count = 0
    for value in range(input[0], input[1] + 1):
        if is_valid_2(value):
            count += 1
    
    return count


def is_valid_2(value):
    last_digit = ''
    two_the_same = False
    mult_count = 0

    for digit in str(value):        
        if digit < last_digit:
            return False

        if digit == last_digit:
            mult_count += 1
        else:
            if mult_count == 2:
                two_the_same = True
            mult_count = 1

        last_digit = digit

    if mult_count == 2:
        two_the_same = True

    return two_the_same


print('Part 1 ', solve1((264793, 803935)))

print('True 111111', is_valid(111111))
print('False 223450', is_valid(223450))
print('False 123789', is_valid(123789))


print('True 112233', is_valid_2(112233))
print('False 123444', is_valid_2(123444))
print('True 111122', is_valid_2(111122))

print('Part 2 ', solve2((264793, 803935)))