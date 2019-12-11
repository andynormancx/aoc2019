#!/usr/local/bin/python3
import InputHelper as IH
from collections import defaultdict

verbose = False
class Instruction():
    def __init__(self, raw):
        self.raw = raw
        self.op_code = None
        self.param_count = 0
        self.param_modes = []
        self.mode_map = {
            '': 'position',
            '0': 'position',
            '1': 'immediate',
            '2': 'relative',
        }
        self.op_code_map = {
            '1': ('add', 3, 4),
            '2': ('mult', 3, 4),
            '3': ('in', 1, 2),
            '4': ('out', 1, 2),
            '5': ('jump-if-true', 2, 3),
            '6': ('jump-if-false', 2, 3),
            '7': ('less than', 3, 4),
            '8': ('equals', 3, 4),
            '9': ('adj-rel-base', 1, 2)
        }
        self.length = 1
        self.decode()

    def __repr__(self):
        return f'{self.raw} {self.op_code}  params_count: {self.param_count} param_modes: {self.param_modes}'

    def decode(self):
        if self.raw[-2:] == '99':
            self.op_code = 'halt'
            return
    
        self.op_code, self.param_count, self.length = self.op_code_map[self.raw[-1]]

        for param_index in range(0, self.param_count):
            self.param_modes.append(self.mode_map[self.raw[-3 - param_index:-2 - param_index]])
        
def solve1(input):
    dirs = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]
    dir_index = 0
    position = (0,0)
    locations = defaultdict(int)
    panels_painted = set()

    vm = VM(convert(input), [0], name = 'Day 11.1')
    output_state = 'paint'

    while vm.running:
        print(vm.inputs)
        vm.run()
        print(vm.state)
        if vm.state == 'output':
            if output_state == 'paint':
                print('paint')
                locations[position] = vm.last_output
                panels_painted.add(position)
                output_state = 'move'
            else:
                print('move')
                if vm.last_output == 0:
                    dir_index = (dir_index - 1) % 4
                else:
                    dir_index = (dir_index + 1) % 4
                position = (position[0] + dirs[dir_index][0], position[1] + dirs[dir_index][1])
                vm.inputs.clear()
                vm.inputs.append(locations[position])
                output_state = 'paint'
        elif vm.state == 'input':
            print('input')
            vm.inputs.append(locations[position])

    print(len(panels_painted))

def solve2(input):
    dirs = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]
    dir_index = 0
    position = (0,0)
    locations = defaultdict(int)
    panels_painted = set()

    vm = VM(convert(input), [1], name = 'Day 11.2')
    output_state = 'paint'

    while vm.running:
        print(vm.inputs)
        vm.run()
        print(vm.state)
        if vm.state == 'output':
            if output_state == 'paint':
                print('paint')
                locations[position] = vm.last_output
                panels_painted.add(position)
                output_state = 'move'
            else:
                print('move')
                if vm.last_output == 0:
                    dir_index = (dir_index - 1) % 4
                else:
                    dir_index = (dir_index + 1) % 4
                position = (position[0] + dirs[dir_index][0], position[1] + dirs[dir_index][1])
                vm.inputs.clear()
                vm.inputs.append(locations[position])
                output_state = 'paint'
        elif vm.state == 'input':
            print('input')
            vm.inputs.append(locations[position])

    print(locations)

    for y in range(0, 6):
        for x in range(0, 42):
            if locations[(x, y)] == 0:
                print('_', end='')
            else:
                print('#', end='')
        print(' end')

class VM():
    def __init__(self, memory, inputs, name):
        self.memory = memory
        self.ip = 0
        self.rel_base = 0
        self.inputs = inputs
        self.target_vm = None
        self.last_output = None
        self.running = True
        self.name = name
        self.outputs = []
        self.state = 'init'
    
    def run(self):
        if not self.running:
            print(f'{self.name} halted')
            return

        output, state, self.memory, self.ip, self.rel_base = run_prog(self.memory, self.inputs, self.ip, self.rel_base, self.name)

        if state == 'output':
            if not self.target_vm == None:
                self.target_vm.add_input(output)
            self.last_output = output
            self.outputs.append(output)
            #print(f'Amp {self.name} output {output}')
            self.state = 'output'
        elif state == 'halted':
            self.running = False
            print(f'{self.name} halted')
            print(self.outputs)
            self.state = 'halted'
        else:
            self.state = 'input'
            print(f'{self.name} paused')

    def add_input(self, input):
        self.inputs.append(input)

    def set_target_vm(self, target_vm):
        self.target_vm = target_vm

def run_prog(codes, input_values, ip = None, rel_base = 0, name = 'Unknown'):
    running = True
    if not ip == None:
        index = ip
    else:
        index = 0

    if not rel_base == None:
        rel_base_ip = rel_base
    else:
        rel_base_ip = 0

    state = 'running'
    output_value = None

    if isinstance(codes, list):
        codes_dict = defaultdict(int)

        for code_index, code in enumerate(codes):
            codes_dict[code_index] = code

        codes = codes_dict

    while running:
        instruction = Instruction(str(codes[index]))
        if verbose: print(instruction)
        if verbose: print(f'rel_base_ip: {rel_base_ip}')
        jumped = False

        if instruction.op_code == 'halt':
            running = False
            state = 'halted'
            continue

        lh_value = None
        rh_value = None
        target_index = None

        if instruction.param_count == 3:
            if instruction.param_modes[0] == 'position':
                lh_value = codes[codes[index + 1]]
            elif instruction.param_modes[0] == 'relative':
                lh_value = codes[codes[index + 1] + rel_base_ip]
            else:
                lh_value = codes[index + 1]

            if instruction.param_modes[1] == 'position':
                rh_value = codes[codes[index + 2]]
            elif instruction.param_modes[1] == 'relative':
                rh_value = codes[codes[index + 2] + rel_base_ip]
            else:
                rh_value = codes[index + 2]

            if instruction.param_modes[2] == 'position':
                target_index = codes[index + 3]
            elif instruction.param_modes[2] == 'relative':
                target_index = codes[index + 3] + rel_base_ip
            else:
                print('Unsupported immediate for output param')

            if instruction.op_code == 'add':
                if verbose: print(f'Adding {lh_value} + {rh_value} to loc {target_index}')
                codes[target_index] = lh_value + rh_value
            elif instruction.op_code == 'mult':
                if verbose: print('Multing ', lh_value * rh_value, ' to loc ', target_index)
                codes[target_index] = lh_value * rh_value
            elif instruction.op_code == 'less than':
                if verbose: print('Less than ', lh_value < rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value < rh_value else 0
            elif instruction.op_code == 'equals':
                if verbose: print('Equals ', lh_value == rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value == rh_value else 0
            else:
                print('Unsupported op_code (3)')
        elif instruction.param_count == 2:
            if instruction.param_modes[0] == 'position':
                lh_value = codes[codes[index + 1]]
            elif instruction.param_modes[0] == 'relative':
                lh_value = codes[codes[index + 1] + rel_base_ip]
            else:
                lh_value = codes[index + 1]
            if instruction.param_modes[1] == 'position':
                rh_value = codes[codes[index + 2]]
            elif instruction.param_modes[1] == 'relative':
                rh_value = codes[codes[index + 2] + rel_base_ip]
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
                if len(input_values) == 0:
                    state = 'paused'
                elif instruction.param_modes[0] == 'position':
                    input_value = input_values.pop(0)
                    if verbose: print('In ', input_value, ' to ', target_index)
                    codes[target_index] = input_value
                elif instruction.param_modes[0] == 'relative':
                    input_value = input_values.pop(0)
                    if verbose: print('In ', input_value, ' to ', target_index + rel_base_ip)
                    codes[target_index + rel_base_ip] = input_value
            elif instruction.op_code == 'out':
                if instruction.param_modes[0] == "immediate":
                    output_value = codes[index + 1]
                    running = False
                    state = 'output'
                    if verbose: print('Out ', output_value)
                elif instruction.param_modes[0] == 'position':
                    output_value = codes[target_index]
                    running = False
                    state = 'output'
                    if verbose: print('Out ', output_value)
                else:
                    output_value = codes[target_index + rel_base_ip]
                    running = False
                    state = 'output'
                    if verbose: print('Out ', output_value)
            elif instruction.op_code == 'adj-rel-base':
                rel_base_old = rel_base_ip

                if instruction.param_modes[0] == "immediate":
                    rel_base_ip += codes[index + 1]
                elif instruction.param_modes[0] == 'position':
                    rel_base_ip += codes[target_index]
                else:
                    rel_base_ip += codes[target_index + rel_base_ip]

                if verbose: print(f'Adj rel base from {rel_base_old} to {rel_base_ip}')
            else:
                print('Unsupported op_code (1)')
        else:
            print('Unsupported param_count')
            quit()

        if not jumped and not state == 'paused': # need to stay on input instruction if waiting on input
            index += instruction.length

    return output_value, state, codes, index, rel_base_ip

def convert(lines):
    return [int(line) for line in lines.split(',')]

data = IH.InputHelper(11).readlines()

#print('Part 1 ', solve1(data[0]))
print('Part 2 ', solve2(data[0]))
quit()

#print(Instruction('11101'))

# mult
print(run_prog([109,19,1102,3,3,1985,204,-34,99], [], 0, 2000))
print(run_prog([109,19,1202,-2019,3,1985,204,-34,99], [], 0, 2000))
# add
print(run_prog([109,19,1201,-2019,3,1985,204,-34,99], [], 0, 2000))
# out
print(run_prog([109,19,2201,-2019,-2018,1985,204,-34,99], [], 0, 2000))
# in
print(run_prog([109,19,203,-34,99], [657132], 0, 2000))

quit()
#vm = VM([104,1125899906842624,99], [], 'Day 9')
#vm = VM([1102,34915192,34915192,7,4,7,99,0], [], 'Day 9')
vm = VM([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [], name = 'Day 9')

while vm.running:
    vm.run()

print(vm.outputs)

#print('Part 2 ', solve2(data[0]))
#solve2('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
#print('Part 1 ', solve1(data))
#print('2,0,0,0,99 ', solve1('1,0,0,0,99'))
#print('2,3,0,6,99 ', solve1('2,3,0,3,99'))
#print('2,4,4,5,99,9801 ', solve1('2,4,4,5,99,0'))
#print('1,1,1,4,99,5,6,0,99 ', solve1('1,1,1,4,99,5,6,0,99'))

#print('Part 2 ', solve2(data[0]))
#print(run_prog([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 5))
#run_prog([3,9,8,9,10,9,4,9,99,-1,8 ], 6)