#!/usr/local/bin/python3
import InputHelper as IH

def solve1(input):
    codes = convert(input)

    codes[1] = 12
    codes[2] = 2

    return run_prog(codes)

def run_prog(codes):
    running = True
    index = 0

    while running:
        opcode = codes[index]

        if opcode == 99:
            running = False
            continue

        lh_index = codes[index + 1]
        rh_index = codes[index + 2]
        target_index = codes[index + 3]

        if opcode == 1:
            codes[target_index] = codes[lh_index] + codes[rh_index]

        if opcode == 2:
            codes[target_index] = codes[lh_index] * codes[rh_index]
        
        index += 4

    return codes[0]    

def solve2(input):
    codes = convert(input)

    for noun in range(0, 99):
        for verb in range(0, 99):
            new_codes = codes[:]
            new_codes[1] = noun
            new_codes[2] = verb
            output = run_prog(new_codes)
            if output == 19690720:
                return (noun, verb)
    
    return 'not found'

def convert(lines):
    return [int(line) for line in lines.split(',')]


data = IH.InputHelper(2).readlines()

print('Part 1 ', solve1(data[0]))
#print('Part 1 ', solve1(data))
#print('2,0,0,0,99 ', solve1('1,0,0,0,99'))
#print('2,3,0,6,99 ', solve1('2,3,0,3,99'))
#print('2,4,4,5,99,9801 ', solve1('2,4,4,5,99,0'))
#print('1,1,1,4,99,5,6,0,99 ', solve1('1,1,1,4,99,5,6,0,99'))

print('Part 2 ', solve2(data[0]))