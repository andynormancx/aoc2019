#!/usr/local/bin/python3
import InputHelper as IH
from collections import defaultdict
from os import system
import sys, os
from collections import deque

verbose = True
vm_verbose = False

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


class Nic():
    def __init__(self, code, router, address):
        if verbose: print(f'Creating nic {address}')
        self.address = address
        self.router = router
        self.vm = VM(code.copy(), [address], name = 'Day 23.1 ' + str(address))
        self.input_queue = deque()
        self.output_state = 'waiting address'
        self.output_address = None
        self.output_x = None
        self.output_y = None        

    def run(self):            
        self.vm.run()

        if self.vm.state == 'output':
            if self.output_state == 'waiting address':
                if verbose: print(f'nic {self.address} receiving address: {self.vm.last_output}')
                self.output_address = int(self.vm.last_output)
                self.output_state = 'waiting x'
            elif self.output_state == 'waiting x':
                if verbose: print(f'nic {self.address} receiving x: {self.vm.last_output}')
                self.output_x = int(self.vm.last_output)
                self.output_state = 'waiting y'
            elif self.output_state == 'waiting y':
                if verbose: print(f'nic {self.address} receiving y: {self.vm.last_output}')
                self.output_y = int(self.vm.last_output)
                self.output_state = 'waiting address'
                self.router.route_packet(self.output_address, (self.output_x, self.output_y))
        elif self.vm.state == 'input':
            try:
                packet = self.input_queue.pop()
                if verbose: print(f'nic {self.address} sending x: {packet[0]} y: {packet[1]}')
                self.vm.inputs.append(packet[0])
                self.vm.inputs.append(packet[1])
            except IndexError:
                if verbose: print(f'nic {self.address} nothing to send')
                self.vm.inputs.append(-1)
                return True
        
        return False
        
    def send_packet(self, packet):
        self.input_queue.append(packet)

class Router():
    def __init__(self, code, num_nics):
        self.nics = {}
        self.num_nics = num_nics
        self.code = code
        self.create_nics()
        self.last_nic_packet = None

    def create_nics(self):
        for index in range(self.num_nics):
            self.nics[index] = Nic(self.code, self, index)

    def run(self):
        idle_last_time = False
        last_sent_nic_packet = None

        while True:
            num_idle = 0
            for nic in self.nics.values():
                if nic.run():
                    num_idle += 1
            if num_idle == 50:
                if idle_last_time: # hack ?
                    print(f'idle: {self.last_nic_packet}')
                    idle_last_time = False
                    if not(last_sent_nic_packet == None) and last_sent_nic_packet == self.last_nic_packet:
                        quit()
                    else:
                        last_sent_nic_packet = self.last_nic_packet
                        self.nics[0].send_packet(self.last_nic_packet)

                else:
                    idle_last_time = True

    
    def route_packet(self, dst_address, packet):
        if dst_address == 255:
            self.last_nic_packet = packet
            print(f'Found 255: x: {packet[0]} y: {packet[1]}')
        else:
            self.nics[dst_address].send_packet(packet)


def solve1(input):
    code = convert(input)

    router = Router(code, 50)
    router.run()

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
            #print(self.outputs)
            self.state = 'halted'
        else:
            self.state = 'input'
            if vm_verbose: print(f'{self.name} paused')

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
        if vm_verbose: print(instruction)
        if vm_verbose: print(f'rel_base_ip: {rel_base_ip}')
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
                if vm_verbose: print(f'Adding {lh_value} + {rh_value} to loc {target_index}')
                codes[target_index] = lh_value + rh_value
            elif instruction.op_code == 'mult':
                if vm_verbose: print('Multing ', lh_value * rh_value, ' to loc ', target_index)
                codes[target_index] = lh_value * rh_value
            elif instruction.op_code == 'less than':
                if vm_verbose: print('Less than ', lh_value < rh_value, ' to loc ', target_index)
                codes[target_index] = 1 if lh_value < rh_value else 0
            elif instruction.op_code == 'equals':
                if vm_verbose: print('Equals ', lh_value == rh_value, ' to loc ', target_index)
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
                    if vm_verbose: print(f'Jumping to {rh_value} from {index}')
                    index = rh_value
                    jumped = True
            elif instruction.op_code == 'jump-if-false':
                if lh_value == 0:
                    if vm_verbose: print(f'Jumping to {lh_value} from {index}')
                    index = rh_value
                    jumped = True
            else:
                print('Unsupported op_code (2)')

        elif instruction.param_count == 1:
            target_index = codes[index + 1]
            
            if instruction.op_code == 'in':
                if len(input_values) == 0:
                    state = 'paused'
                    running = False
                elif instruction.param_modes[0] == 'position':
                    input_value = input_values.pop(0)
                    if vm_verbose: print('In ', input_value, ' to ', target_index)
                    codes[target_index] = input_value
                elif instruction.param_modes[0] == 'relative':
                    input_value = input_values.pop(0)
                    if vm_verbose: print('In ', input_value, ' to ', target_index + rel_base_ip)
                    codes[target_index + rel_base_ip] = input_value
            elif instruction.op_code == 'out':
                if instruction.param_modes[0] == "immediate":
                    output_value = codes[index + 1]
                    running = False
                    state = 'output'
                    if vm_verbose: print('Out ', output_value)
                elif instruction.param_modes[0] == 'position':
                    output_value = codes[target_index]
                    running = False
                    state = 'output'
                    if vm_verbose: print('Out ', output_value)
                else:
                    output_value = codes[target_index + rel_base_ip]
                    running = False
                    state = 'output'
                    if vm_verbose: print('Out ', output_value)
            elif instruction.op_code == 'adj-rel-base':
                rel_base_old = rel_base_ip

                if instruction.param_modes[0] == "immediate":
                    rel_base_ip += codes[index + 1]
                elif instruction.param_modes[0] == 'position':
                    rel_base_ip += codes[target_index]
                else:
                    rel_base_ip += codes[target_index + rel_base_ip]

                if vm_verbose: print(f'Adj rel base from {rel_base_old} to {rel_base_ip}')
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

data = IH.InputHelper(23).readlines()

print('Part 1 ', solve1(data[0]))
#print('Part 2 ', solve2(data[0]))
quit()