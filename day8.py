#!/usr/local/bin/python3
import InputHelper as IH
import sys
import itertools
verbose = True

def solve1(input):
    layers = []
    pixels_per_layer = 25 * 6

    for index in range(0, len(input), pixels_per_layer):
        #print(f'{index}')
        layers.append(input[index:index + pixels_per_layer])

    min_count = sys.maxsize
    min_layer = None
    for layer in layers:
        count = count_digits(layer, '0')
        if count < min_count:
            min_layer = layer
            min_count = count

    print(count_digits(min_layer, '1') * count_digits(min_layer, '2') )

    image = list(' ' * pixels_per_layer)

    layers = list(reversed(layers))

    for layer_index in range(0, len(layers)):
        for pixel_index, pixel in enumerate(layers[layer_index]):
            if pixel == '0':
                image[pixel_index] = '_'
            if pixel == '1':
                image[pixel_index] = '*'

    output_rows = [image[i:i + 25] for i in range(len(image))[::25]]
    
    [print(''.join(x)) for x in output_rows]
    print()

    for row_index in range(0, 6):
        row = image[row_index * 25 : row_index * 25 + 25]
        print(''.join(row))

def count_digits(layer, digit):
    return len(list(filter(lambda x: x == digit, list(layer))))

data = IH.InputHelper(8).readlines()

#run_prog([3,0,4,0,99], 1)

print('Part 1 ', solve1(data[0]))
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