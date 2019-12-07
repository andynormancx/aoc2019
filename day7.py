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

    max_signal = 0
    a_phases = set([0, 1, 2, 3, 4])

    for a_phase in a_phases:
        b_phases = a_phases - set([a_phase])
        for b_phase in b_phases:
            c_phases = b_phases - set([b_phase])
            for c_phase in c_phases:
                d_phases = c_phases - set([c_phase])
                for d_phase in d_phases:
                    e_phases = d_phases - set([d_phase])
                    e_phase = e_phases.pop()
                    print(f'a: {a_phase} b: {b_phase} c: {c_phase} d: {d_phase} e: {e_phase}')

                    signal = 0
                    signal, *_ = run_prog(codes.copy() , [a_phase, signal])
                    signal, *_ = run_prog(codes.copy() , [b_phase, signal])
                    signal, *_ = run_prog(codes.copy() , [c_phase, signal])
                    signal, *_ = run_prog(codes.copy() , [d_phase, signal])
                    signal, *_ = run_prog(codes.copy() , [e_phase, signal])

                    max_signal = signal if signal > max_signal else max_signal
    print(max_signal)
    return max_signal

def solve2(input):
    codes = convert(input)

    max_signal = 0
    a_phases = set([5, 6, 7, 8, 9])

    for a_phase in a_phases:
        b_phases = a_phases - set([a_phase])
        for b_phase in b_phases:
            c_phases = b_phases - set([b_phase])
            for c_phase in c_phases:
                d_phases = c_phases - set([c_phase])
                for d_phase in d_phases:
                    e_phases = d_phases - set([d_phase])
                    e_phase = e_phases.pop()

                    a_phase = 9
                    b_phase = 8
                    c_phase = 7
                    d_phase = 6
                    e_phase = 5

                    print(f'a: {a_phase} b: {b_phase} c: {c_phase} d: {d_phase} e: {e_phase}')

                    signal = 0

                    a_vm = VM(codes.copy(), [a_phase, signal], 'A')
                    b_vm = VM(codes.copy(), [b_phase, signal], 'B')
                    c_vm = VM(codes.copy(), [c_phase, signal], 'C')
                    d_vm = VM(codes.copy(), [d_phase, signal], 'D')
                    e_vm = VM(codes.copy(), [e_phase, signal], 'E')

                    a_vm.set_target_vm(b_vm)
                    b_vm.set_target_vm(c_vm)
                    c_vm.set_target_vm(d_vm)
                    d_vm.set_target_vm(e_vm)
                    e_vm.set_target_vm(a_vm)

                    while a_vm.running or b_vm.running or c_vm.running or d_vm.running or e_vm.running:
                        a_vm.run()
                        b_vm.run()
                        c_vm.run()
                        d_vm.run()
                        e_vm.run()
                    
                    print(f'Last output from e {e_vm.last_output}')
                    max_signal = max(max_signal, e_vm.last_output)
                    return
    print(f'Max signal {max_signal}')
    return max_signal

class VM():
    def __init__(self, memory, inputs, name):
        self.memory = memory
        self.ip = 0
        self.inputs = inputs
        self.target_vm = None
        self.last_output = None
        self.running = True
        self.name = name

    def run(self):
        if not self.running:
            print(f'{self.name} halted')
            return

        output, state, self.memory, self.ip = run_prog(self.memory, self.inputs, self.ip)

        if state == 'output':
            self.target_vm.add_input(output)
            self.last_output = output
            print(f'Amp {self.name} output {output}')
        elif state == 'halted':
            self.running = False
            print(f'{self.name} halted')
        else:
            print(f'{self.name} paused')

    def add_input(self, input):
        self.inputs.append(input)

    def set_target_vm(self, target_vm):
        self.target_vm = target_vm

def run_prog(codes, input_values, ip = None):
    #print(codes)
    #print(input_values)
    #print(ip)
    running = True
    if not ip == None:
        index = ip
    else:
        index = 0

    state = 'running'
    output_value = None

    #print(len(codes), ' memory locations')
    while running:
        instruction = Instruction(str(codes[index]))
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
                #print(f'Adding {lh_value} + {rh_value} to loc {target_index}')
                codes[target_index] = lh_value + rh_value
            elif instruction.op_code == 'mult':
                #print('Multing ', lh_value * rh_value, ' to loc ', target_index)
                codes[target_index] = lh_value * rh_value
            elif instruction.op_code == 'less than':
                #print('Less than ', lh_value < rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value < rh_value else 0
            elif instruction.op_code == 'equals':
                #print('Equals ', lh_value == rh_value, ' to loc ', target_index)
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
                if len(input_values) == 0:
                    state = 'paused'
                else:
                    input_value = input_values.pop(0)
                    #print('In ', input_value, ' to ', target_index)
                    codes[target_index] = input_value
            elif instruction.op_code == 'out':
                if instruction.param_modes[0] == "immediate":
                    output_value = codes[index + 1]
                    running = False
                    state = 'output'
                else:
                    output_value = codes[target_index]
                    running = False
                    state = 'output'
            else:
                print('Unsupported op_code (1)')
        else:
            print('Unsupported param_count')
            quit()

        if not jumped and not state == 'paused': # need to stay on input instruction if waiting on input
            index += instruction.length

    #print(input_values)
    return output_value, state, codes, index

def convert(lines):
    return [int(line) for line in lines.split(',')]

data = IH.InputHelper(7).readlines()

#run_prog([3,0,4,0,99], 1)

#print('Part 1 ', solve1(data[0]))
print('Part 2 ', solve2(data[0]))
solve2('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5')
#print('Part 1 ', solve1(data))
#print('2,0,0,0,99 ', solve1('1,0,0,0,99'))
#print('2,3,0,6,99 ', solve1('2,3,0,3,99'))
#print('2,4,4,5,99,9801 ', solve1('2,4,4,5,99,0'))
#print('1,1,1,4,99,5,6,0,99 ', solve1('1,1,1,4,99,5,6,0,99'))

#print('Part 2 ', solve2(data[0]))
#print(run_prog([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 5))
#run_prog([3,9,8,9,10,9,4,9,99,-1,8 ], 6)