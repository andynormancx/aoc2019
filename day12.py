#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math
from functools import reduce

verbose = True

def solve1(input):
    positions = input
    velocities  = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    # gravity
    for _ in range(1000):
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

        if verbose:
            print(_)
            for pos in positions:
                print(f'x = {pos[0]} y = {pos[1]} z = {pos[2]}')
            print()
            for vel in velocities:
                print(f'x = {vel[0]} y = {vel[1]} z = {vel[2]}')
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
    seen = set()
    pos_seen = set()
    vel_seen = set()
    running = True
    while running:
        step += 1
        if step == 2772:
            running = False
        if step % 100000 == 0:
            print(step)
            for pos in positions:
                print(f'x = {pos[0]} y = {pos[1]} z = {pos[2]}')
            print()
            for vel in velocities:
                print(f'x = {vel[0]} y = {vel[1]} z = {vel[2]}')
            print()

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

        pos_state = (positions[0][0], positions[0][1], positions[0][2], positions[1][0], positions[1][1], positions[1][2], positions[2][0], positions[2][1], positions[2][2])

        if pos_state in pos_seen:
            print(f'Seen pos at {step}')
        pos_seen.add(pos_state)

        vel_state = (velocities[0][0], velocities[0][1], velocities[0][2], velocities[1][0], velocities[1][1], velocities[1][2], velocities[2][0], velocities[2][1], velocities[2][2])

        if vel_state in vel_seen:
            print(f'Seen vels at {step}')
        vel_seen.add(vel_state)

        state = ''
        for moon_index, moon in enumerate(positions):
            state += str(moon[0] + moon[1] * 10 + moon[2] * 100 + velocities[moon_index][0] * 1000 + velocities[moon_index][1] * 10000 + velocities[moon_index][2] * 100000) + '_'
            moon[0] += velocities[moon_index][0]
            moon[1] += velocities[moon_index][1]
            moon[2] += velocities[moon_index][2]
        
        if state in seen:
            print(f'Done {step}')
            running = False

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

# example
data = [
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]
]
#quit()
#print('Part 1 ', solve1(data))
print('Part 2 ', solve2(data))
