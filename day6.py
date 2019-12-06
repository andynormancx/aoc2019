#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections


def solve1(input):
    lines = convert(input)
    bodies = {}
    orbits = 0

    for left, right in lines:
        bodies[right] = left

    for body in bodies.keys():
        orbits += count_orbits(bodies, body)

    print(orbits)

def count_orbits(bodies, body):
    count = 0
    while body != 'COM':
        count += 1
        body = bodies[body]

    return count

def get_orbits(bodies, body):
    orbits = []
    while body != 'COM':
        orbits.append(body)
        body = bodies[body]

    return set(orbits)

def solve2(input):
    lines = convert(input)
    bodies = {}
    orbits = 0

    for left, right in lines:
        bodies[right] = left

    for body in bodies.keys():
        orbits += count_orbits(bodies, body)

    you = get_orbits(bodies, 'YOU')
    san = get_orbits(bodies, 'SAN')
    print(len(you ^ san) - 2)

def convert(lines):
    return [line.split(')') for line in lines]


data = IH.InputHelper(6).readlines()


print('Part 1 ', solve1(data))
print('Part 1 ', solve2(data))

