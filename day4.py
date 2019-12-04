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
    digits = [int(digit) for digit in str(value)]
    last_digit = 0
    two_the_same = False
    mult_count = 0

    for digit in digits:
        if digit < last_digit:
            return False
        
        if digit == last_digit:
            mult_count += 1
            #print(str(digit) + ' ' + str(mult_count), ' same')
        else:
            #print(str(digit) + ' ' + str(mult_count), ' NOT same')
            if mult_count == 2:
                two_the_same = True
            mult_count = 1

        last_digit = digit

    if mult_count == 2:
        two_the_same = True

    #print()

    return two_the_same


print('Part 1 ', solve1((264793, 803935)))

print('True 111111', is_valid(111111))
print('False 223450', is_valid(223450))
print('False 123789', is_valid(123789))


print('True 112233', is_valid_2(112233))
print('False 123444', is_valid_2(123444))
print('True 111122', is_valid_2(111122))

print('Part 2 ', solve2((264793, 803935)))


#print('6 3,3', solve1(['R8,U5,L5,D3', 'U7,R6,D4,L4']))



#print('159 610', solve1(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']))

#print('135 410', solve1(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))


