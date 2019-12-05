#!/usr/local/bin/python3
import InputHelper as IH

class Instruction():
    def __init__(self, raw):
        self.raw = raw
        self.op_code = None
        self.mode = None
        self.param_count = 0
        self.param_modes = []
        self.mode_map = {
            '': 'position',
            '0': 'position',
            '1': 'immediate'
        }
        self.op_code_map = {
            '1': ('add', 3, 4),
            '2': ('mult', 3, 4),
            '3': ('in', 1, 2),
            '4': ('out', 1, 2),
            '5': ('jump-if-true', 2, 3),
            '6': ('jump-if-false', 2, 3),
            '7': ('less than', 3, 4),
            '8': ('equals', 3, 4)
        }
        self.length = 1
        self.decode()

    def decode(self):
        if self.raw[-2:] == '99':
            self.op_code = 'halt'
            return
    
        self.op_code, self.param_count, self.length = self.op_code_map[self.raw[-1]]
        self.mode = self.mode_map[self.raw[-2:-1]]

        for param_index in range(0, self.param_count):
            self.param_modes.append(self.mode_map[self.raw[-3 - param_index:-2 - param_index]])
        
def solve1(input):
    codes = convert(input)

    return run_prog(codes, 1)

def run_prog(codes, input_value):
    running = True
    index = 0

    print(len(codes), ' memory locations')
    while running:
        instruction = Instruction(str(codes[index]))
        jumped = False

        #print(codes[index], instruction.op_code, instruction.param_count, instruction.mode, instruction.param_modes, instruction.length)
        #print(codes[index:index + instruction.length])
        #print(codes[0:20])
        print(codes)

        if instruction.op_code == 'halt':
            running = False
            continue

        lh_value = None
        rh_value = None
        target_index = None

        if instruction.param_count == 3:
            if instruction.param_modes[0] == 'position':
                lh_value = codes[codes[index + 1]]
            else:
                lh_value = codes[index + 1]

            if instruction.param_modes[1] == 'position':
                rh_value = codes[codes[index + 2]]
            else:
                rh_value = codes[index + 2]

            if instruction.param_modes[2] == 'position':
                target_index = codes[index + 3]
            else:
                print('Unsupported immediate for output param')

            if instruction.op_code == 'add':
                print('Adding ', lh_value + rh_value, ' to loc ', target_index)
                codes[target_index] = lh_value + rh_value
            elif instruction.op_code == 'mult':
                print('Multing ', lh_value * rh_value, ' to loc ', target_index)
                codes[target_index] = lh_value * rh_value
            elif instruction.op_code == 'less than':
                print('Less than ', lh_value < rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value < rh_value else 0
            elif instruction.op_code == 'equals':
                print('Equals ', lh_value == rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value == rh_value else 0
            else:
                print('Unsupported op_code (3)')
        elif instruction.param_count == 2:
            if instruction.param_modes[0] == 'position':
                lh_value = codes[codes[index + 1]]
            else:
                lh_value = codes[index + 1]
            if instruction.param_modes[1] == 'position':
                rh_value = codes[codes[index + 2]]
            else:
                rh_value = codes[index + 2]

            if instruction.op_code == 'jump-if-true':
                if lh_value != 0:
                    index = rh_value
                    jumped = True
            elif instruction.op_code == 'jump-if-false':
                if lh_value == 0:
                    index = rh_value
                    jumped = True
            else:
                print('Unsupported op_code (2)')

        elif instruction.param_count == 1:
            target_index = codes[index + 1]
            
            if instruction.op_code == 'in':
                print('In ', input_value, ' to ', target_index)
                codes[target_index] = input_value
            elif instruction.op_code == 'out':
                if instruction.param_modes[0] == "immediate":
                    print('Output (immediate): ', codes[index + 1])
                else:
                    output_value = codes[target_index]
                    print('Out ', output_value, ' from ', target_index)
                    print('Output: ', output_value)
            else:
                print('Unsupported op_code (1)')
        else:
            print('Unsupported param_count')
            quit()

        if not jumped:
            index += instruction.length

    return codes[0]    

def solve2(input):
    codes = convert(input)

    return run_prog(codes, 5)

def convert(lines):
    return [int(line) for line in lines.split(',')]

data = IH.InputHelper(5).readlines()

halt = Instruction('99')
#print(halt.op_code, halt.param_count)

inputIns = Instruction('13')
#print(inputIns.op_code, inputIns.param_count, inputIns.mode, inputIns.param_modes, inputIns.length)

multIns = Instruction('12')
#print(multIns.op_code, multIns.param_count, multIns.mode, multIns.param_modes, multIns.length)

multInsPos = Instruction('0102')
#print(multInsPos.op_code, multInsPos.param_count, multInsPos.mode, multInsPos.param_modes, multInsPos.length)

#run_prog([3,0,4,0,99], 1)

#print('Part 1 ', solve1(data[0]))
#print('Part 1 ', solve1(data))
#print('2,0,0,0,99 ', solve1('1,0,0,0,99'))
#print('2,3,0,6,99 ', solve1('2,3,0,3,99'))
#print('2,4,4,5,99,9801 ', solve1('2,4,4,5,99,0'))
#print('1,1,1,4,99,5,6,0,99 ', solve1('1,1,1,4,99,5,6,0,99'))

#print('Part 2 ', solve2(data[0]))
#print(run_prog([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 5))
run_prog([3,9,8,9,10,9,4,9,99,-1,8 ], 6)