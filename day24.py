#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math
from functools import reduce
from sympy import ilcm
from copy import deepcopy

verbose = False


def solve1(input):
    cells = {}

    for row_index, row in enumerate(input):
        for col_index, col in enumerate(row):
            cells[(row_index, col_index)] = col
    
    print_cells(cells, 5, 5)

    bios_seen = set()
    bios_seen.add(calc_bio(cells, 5, 5))
    step = 1
    while True:
        new_cells = {}
        for cell_key, cell in cells.items():
            live_neighbours_count = len(list(filter(lambda x: cells[x] == '#', get_neighbours_keys(cell_key, 5, 5))))
            if cell == '#':
                if live_neighbours_count == 1:
                    if verbose: print(f'{cell_key} lives {live_neighbours_count}')
                    new_cells[cell_key] = '#'
                else:
                    if verbose: print(f'{cell_key} dies  {live_neighbours_count}')
                    new_cells[cell_key] = '.'
            else:
                if live_neighbours_count >= 1 and live_neighbours_count <= 2:
                    if verbose: print(f'{cell_key} born  {live_neighbours_count}')
                    new_cells[cell_key] = '#'
                else:
                    if verbose: print(f'{cell_key} still {live_neighbours_count}')
                    new_cells[cell_key] = '.'
        bio = calc_bio(new_cells, 5, 5)
        print(f'{step} {bio}')
        print_cells(new_cells, 5, 5)
        print()
        cells = new_cells
        step += 1

        if bio in bios_seen:
            print(bio)
            return
        else:
            bios_seen.add(bio)

    
    return ''

def get_neighbours_keys(row_col, row_count, col_count):
    row = row_col[0]
    col = row_col[1]

    if row - 1 >= 0:
        yield (row - 1, col)
    if row + 1 < row_count:
        yield (row + 1, col)
    if col - 1 >= 0:
        yield (row, col - 1)
    if col + 1 < col_count:
        yield (row, col + 1)

def calc_bio(cells, row_count, col_count):
    bio = 0
    power = 0
    for row_index in range(row_count):
        for col_index in range(col_count):
            if cells[(row_index, col_index)] == '#':
                bio += 2 ** power
                print((row_index, col_index), power)
            power += 1
    return bio

def print_cells(cells, row_count, col_count):
    for row_index in range(row_count):
        for col_index in range(col_count):
            print(cells[(row_index, col_index)], end='')
        print()

def solve2(input):
    print()


data = IH.InputHelper(24).readlines()


print(solve1([
    '....#',
    '#..#.',
    '#..##',
    '..#..',
    '#....'
]))

print(solve1([
    '####.',
    '.###.',
    '.#..#',
    '##.##',
    '###..'
]))


#print('Part 1 ', solve1(data))
#print('Part 2 ', solve2(data))