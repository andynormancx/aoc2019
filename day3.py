#!/usr/local/bin/python3
import InputHelper as IH
import sys

class Wire():
    def __init__(self, moves):
        self.cells_passed = set()
        self.cell_min_steps = {}
        self.moves = moves
        self.calc_path()

    def calc_path(self):
        vectors = {
            'U': (0, 1),
            'D': (0, -1),
            'L': (1, 0),
            'R': (-1, 0)
        }

        x = 0
        y = 0
        steps = 0

        for (direction, distance) in self.moves:
            for pos in range(0, distance):
                steps += 1
                x += vectors[direction][0]
                y += vectors[direction][1]
                self.cells_passed.add((x, y))
                if not((x, y) in self.cell_min_steps):
                    self.cell_min_steps[(x, y)] = steps

def solve1(input):

    wire_paths = convert(input)

    wire_one = Wire(wire_paths[0])
    wire_two = Wire(wire_paths[1])

    crossings = wire_one.cells_passed & wire_two.cells_passed

    min_distance = 1000000000

    for crossing in crossings:
        distance  = calc_dist(crossing, (0, 0))
        if distance < min_distance:
            min_distance = distance

    min_distance_2 = 1000000000
    for crossing in crossings:
        distance  = wire_one.cell_min_steps[crossing] + wire_two.cell_min_steps[crossing]
        if distance < min_distance_2:
            min_distance_2 = distance
    
    return (min_distance, min_distance_2, crossings)

def calc_dist(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two [1])

def convert(lines):
    return [
        convert_line(lines[0]),
        convert_line(lines[1])
    ]
    #return [int(line) for line in lines.split(',')]

def convert_line(line):
    items = line.split(',')

    moves = []

    for item in items:
        moves.append((
            item[0], int(item[1:])
            ))

    return moves

data = IH.InputHelper(3).readlines()

print('Part 1 ', solve1(data))
print('6 3,3', solve1(['R8,U5,L5,D3', 'U7,R6,D4,L4']))

print('159 610', solve1(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']))

print('135 410', solve1(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))


