#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math
from functools import reduce
import numpy as np
from sympy import ilcm

verbose = False

def solve1(input):
    positions = input
    velocities  = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    print()
    print(f'After 0 steps')
    for index, pos in enumerate(positions):
        print(f'pos=<x= {pos[0]}, y=  {pos[1]}, z= {pos[2]}>, ', end='')
        print(f'vel=<x= {velocities[index][0]} y= {velocities[index][1]} z= {velocities[index][2]}>')
    print()


    # gravity
    for _ in range(100):
        compared = set()
        for moon_index, moon in enumerate(positions):
            for moon_inner_index, moon_inner in enumerate(positions):
                if moon_inner_index == moon_index:
                    continue
                if str(moon_inner_index) + ' ' + str(moon_index) in compared:
                    continue

                compared.add(str(moon_inner_index) + ' ' + str(moon_index))
                compared.add(str(moon_index) + ' ' + str(moon_inner_index))

                if moon[0] > moon_inner[0]:
                    velocities[moon_index][0] -= 1
                    velocities[moon_inner_index][0] += 1
                elif moon[0] < moon_inner[0]:
                    velocities[moon_index][0] += 1
                    velocities[moon_inner_index][0] -= 1

                if moon[1] > moon_inner[1]:
                    velocities[moon_index][1] -= 1
                    velocities[moon_inner_index][1] += 1
                elif moon[1] < moon_inner[1]:
                    velocities[moon_index][1] += 1
                    velocities[moon_inner_index][1] -= 1
                
                if moon[2] > moon_inner[2]:
                    velocities[moon_index][2] -= 1
                    velocities[moon_inner_index][2] += 1
                elif moon[2] < moon_inner[2]:
                    velocities[moon_index][2] += 1
                    velocities[moon_inner_index][2] -= 1

        for moon_index, moon in enumerate(positions):
            moon[0] += velocities[moon_index][0]
            moon[1] += velocities[moon_index][1]
            moon[2] += velocities[moon_index][2]

        if verbose and (_ + 1) % 10 == 0:
            print()
            print(f'After {_ + 1} steps')
            for index, pos in enumerate(positions):
                print(f'pos=<x= {pos[0]}, y=  {pos[1]}, z= {pos[2]}>, ', end='')
                print(f'vel=<x= {velocities[index][0]} y= {velocities[index][1]} z= {velocities[index][2]}>')
            print()

    total = 0
    for index, moon_pos in enumerate(positions):
        moon_vel = velocities[index]

        potential = abs(moon_pos[0]) + abs(moon_pos[1]) + abs(moon_pos[2])
        kinetic = abs(moon_vel[0]) + abs(moon_vel[1]) + abs(moon_vel[2])

        if verbose: print(f'pot: {potential} kin: {kinetic}')
        total += potential * kinetic

    print(total)
            
def solve2(input):
    positions = input
    velocities  = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    # gravity
    step = 0
    x_seen = set()
    y_seen = set()
    z_seen = set()
    x_seen_step = None
    y_seen_step = None
    z_seen_step = None

    print()
    print(f'After 0 steps')
    for index, pos in enumerate(positions):
        print(f'pos=<x= {pos[0]}, y=  {pos[1]}, z= {pos[2]}>, ', end='')
        print(f'vel=<x= {velocities[index][0]} y= {velocities[index][1]} z= {velocities[index][2]}>')
    print()

    running = True
    while x_seen_step == None or y_seen_step == None or z_seen_step == None:
        step += 1

        compared = set()
        for moon_index, moon in enumerate(positions):
            for moon_inner_index, moon_inner in enumerate(positions):
                if moon_inner_index == moon_index:
                    continue
                if str(moon_inner_index) + ' ' + str(moon_index) in compared:
                    continue

                compared.add(str(moon_inner_index) + ' ' + str(moon_index))
                compared.add(str(moon_index) + ' ' + str(moon_inner_index))

                if moon[0] > moon_inner[0]:
                    velocities[moon_index][0] -= 1
                    velocities[moon_inner_index][0] += 1
                elif moon[0] < moon_inner[0]:
                    velocities[moon_index][0] += 1
                    velocities[moon_inner_index][0] -= 1

                if moon[1] > moon_inner[1]:
                    velocities[moon_index][1] -= 1
                    velocities[moon_inner_index][1] += 1
                elif moon[1] < moon_inner[1]:
                    velocities[moon_index][1] += 1
                    velocities[moon_inner_index][1] -= 1
                
                if moon[2] > moon_inner[2]:
                    velocities[moon_index][2] -= 1
                    velocities[moon_inner_index][2] += 1
                elif moon[2] < moon_inner[2]:
                    velocities[moon_index][2] += 1
                    velocities[moon_inner_index][2] -= 1

        for moon_index, moon in enumerate(positions):
            moon[0] += velocities[moon_index][0]
            moon[1] += velocities[moon_index][1]
            moon[2] += velocities[moon_index][2]

        x_all = (
                positions[0][0], velocities[0][0],
                positions[1][0], velocities[1][0],
                positions[2][0], velocities[2][0],
                positions[3][0], velocities[3][0]
                )
        if x_all in x_seen and x_seen_step == None:
            x_seen_step = step
            print(f'x: {step}')
        else:
            x_seen.add(x_all)

        y_all = (
                positions[0][1], velocities[0][1],
                positions[1][1], velocities[1][1],
                positions[2][1], velocities[2][1],
                positions[3][1], velocities[3][1]
                )
        if y_all in y_seen and y_seen_step == None:
            y_seen_step = step
            print(f'y: {step}')
        else:
            y_seen.add(y_all)

        z_all = (
                positions[0][2], velocities[0][2],
                positions[1][2], velocities[1][2],
                positions[2][2], velocities[2][2],
                positions[3][2], velocities[3][2]
                )
        if z_all in z_seen and z_seen_step == None:
            z_seen_step = step
            print(f'z: {step}')
        else:
            z_seen.add(z_all)            

        if verbose and (step) % 10 == 0:
            print()
            print(f'After {step} steps')
            for index, pos in enumerate(positions):
                print(f'pos=<x= {pos[0]}, y=  {pos[1]}, z= {pos[2]}>, ', end='')
                print(f'vel=<x= {velocities[index][0]} y= {velocities[index][1]} z= {velocities[index][2]}>')
            print()


    print(x_seen_step)
    print(y_seen_step)
    print(z_seen_step)
    print(ilcm(x_seen_step - 1, y_seen_step - 1, z_seen_step - 1))

data = IH.InputHelper(12).readlines()


#(0, -1) = 0
#(1, 0) = 90
#(0, 1) = 180
#(-1, 0) = 270


#print(angle_between((0,0), (0, -1)))
#print(angle_between((0,0), (1, 0)))
#print(angle_between((0,0), (0, 1)))
#print(angle_between((0,0), (-1, 0)))
#print(angle_between((11, 13), (11, 12)))
#print(angle_between((11, 13), (12, 13)))
#print(angle_between((11, 13), (11, 14)))
#print(angle_between((11, 13), (10, 13)))

data = [
    [-4, -14, 8],
    [1, -8, 10],
    [-15, 2, 1],
    [-17, -17, 16],
]

# example 1
#data = [
#    [-1, 0, 2],
#    [2, -10, -7],
#    [4, -8, 8],
#    [3, 5, -1]
#]

#examle 2
#data = [
#    [-8, -10, 0],
#    [2, -7, 3],
#    [5, 5, 10],
#    [9, -8, -3]
#]
#quit()
#print('Part 1 ', solve1(data))
print('Part 2 ', solve2(data))
#moons = np.array([[17, 5, 1],[-2, -8, 8],[7, -6, 14],[1, -10, 4]])
#velocity = moons*0
#print(moons)
#print(velocity)
