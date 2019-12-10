#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math


def solve1(input):
    asteroids = {}

    for row_index, row in enumerate(input):
        rows = len(input)
        for col_index, col in enumerate(row):
            cols = len(row)
            if col == '#':
                asteroids[(col_index, row_index)] = 0
    
    for point, _ in asteroids.items():
        for search_point, _ in asteroids.items():
            if (point != search_point):
                points = points_along_line(point, search_point)
                blocked = False
                for point_on_line in points:
                    if point_on_line in asteroids:
                        blocked = True
                if not blocked:
                    asteroids[point] = asteroids[point] + 1

    best_count = max(asteroids.values())
    
    station_point = list(filter(lambda x:x[1] == best_count, asteroids.items()))[0][0]

    print(f'{station_point} {best_count}')

    remaining_asteroids = set(asteroids.keys())
    remaining_asteroids.remove(station_point)
    destroy_count = 0

    while(len(remaining_asteroids) > 0):
        visible = sorted(get_visible(remaining_asteroids, station_point), key=lambda x: angle_between(station_point, x))

        for point in visible:
            destroy_count += 1
            print(f'{destroy_count} {point}')
            remaining_asteroids.remove(point)

def solve2(input):

    
    return 1

def get_visible(asteroids, search_point):
    for asteroid in asteroids:
        if (asteroid != search_point):
            points = points_along_line(search_point, asteroid)
            blocked = False
            for point_on_line in points:
                if point_on_line in asteroids:
                    blocked = True
            if not blocked:
                yield asteroid


def points_along_line(start, end):
    len_x = end[0] - start[0]
    len_y = end[1] - start[1]

    gcd = math.gcd(len_x, len_y)
    vector = (int(len_x / gcd), int(len_y / gcd))

    point = (start[0] + vector[0], start[1] + vector[1])

    while point[0] != end[0] or point[1] != end[1]:
        yield point
        point = (point[0] + vector[0], point[1] + vector[1])

data = IH.InputHelper(10).readlines()


#(0, -1) = 0
#(1, 0) = 90
#(0, 1) = 180
#(-1, 0) = 270

def angle_between(p1, p2):
    ang2 = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) # y, x
    return (math.degrees(ang2 % (2 * math.pi)) + 90) % 360

def angle_between2(p1, p2):
    ang1 = math.atan2(p1[0], p1[1]) # y, x
    ang2 = math.atan2(p2[0], p2[1]) # y, x
    return ((math.degrees((ang1 - ang2) % (2 * math.pi)) + 180) % 360)


#print(angle_between((0,0), (0, -1)))
#print(angle_between((0,0), (1, 0)))
#print(angle_between((0,0), (0, 1)))
#print(angle_between((0,0), (-1, 0)))
#print(angle_between((11, 13), (11, 12)))
#print(angle_between((11, 13), (12, 13)))
#print(angle_between((11, 13), (11, 14)))
#print(angle_between((11, 13), (10, 13)))

#quit()
print('Part 1 ', solve1(data))
