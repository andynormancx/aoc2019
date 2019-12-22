#!/usr/local/bin/python3
import InputHelper as IH
import sys
import collections
import math
from functools import reduce
from sympy import ilcm
from sympy import igcd
from sympy import isprime
from sympy import nextprime
from copy import deepcopy
from collections import deque

verbose = False

def solve1(num_cards, input, init_deck = None):
    #print(f'num cards: {num_cards}')
    if init_deck == None:
        deck = list(range(0, num_cards))
    else:
        deck = init_deck.copy()

    if verbose: print('')

    for line in input:
        if line == 'deal into new stack':
            if verbose: print('new stack')
            deck = deal_new_stack(deck)
        elif line.startswith('deal with increment'):
            increment = int(line.split(' ')[-1])
            if verbose: print(f'increment: {increment}')
            deck = deal_with_increment(deck, increment)
        elif line.startswith('cut'):
            cut = int(line.split(' ')[-1])
            deck = cut_deck(deck, cut)
            if verbose: print(f'cut: {cut}')
        if verbose: print(deck)
            

    if verbose: print(deck)

    return deck

def solve2(input):
    num_cards = 10007
    looking_for = None
    deck = list(range(0, num_cards))
    count = 0

    if verbose: print('')

    while True:
        count += 1
        #print(deck.index(2020))
        for line in input:
            if line == 'deal into new stack':
                if verbose: print('new stack')
                deck = deal_new_stack(deck)
            elif line.startswith('deal with increment'):
                increment = int(line.split(' ')[-1])
                if verbose: print(f'increment: {increment}')
                deck = deal_with_increment(deck, increment)
            elif line.startswith('cut'):
                cut = int(line.split(' ')[-1])
                deck = cut_deck(deck, cut)
                if verbose: print(f'cut: {cut}')
            if verbose: print(deck)
        if looking_for == None:
            looking_for = deck.index(2020)
            print(f'looking for: {looking_for}')
        elif deck.index(2020) == looking_for:
            break
        if count % 100 == 0:
            print(count)
            
    
    print(f'repeated after: {count}')

    #if verbose: print(deck)

    return count

def cut_deck(deck, cut_position):
    return list(deck[cut_position:] + deck[0:cut_position])

def deal_with_increment(deck, increment):
    table = {}

    deck_position = 0
    table_position = 0
    num_cards = len(deck)

    for card in deck:
        table[table_position] = card
        table_position = (table_position + increment) % num_cards

    new_deck = []
    for index in range(0, num_cards):
        new_deck.append(table[index])

    return new_deck

def deal_new_stack(deck):
    return list(reversed(deck))


data = IH.InputHelper(22).readlines()


print(deal_new_stack(list(range(0, 10))))
print(deal_with_increment(list(range(0, 10)), 1))
print(cut_deck(list(range(0, 10)), 3))
print(cut_deck(list(range(0, 10)), -4))
print(deal_with_increment(list(range(0, 10)), 3))
print('0 3 6 9 2 5 8 1 4 7 ', solve1(10, [
    'deal with increment 7',
    'deal into new stack',
    'deal into new stack'
]))

print('3 0 7 4 1 8 5 2 9 6 ', solve1(10, [
    'cut 6',
    'deal with increment 7',
    'deal into new stack'
]))

print('9 2 5 8 1 4 7 0 3 6 ', solve1(10, [
    'deal into new stack',
    'cut -2',
    'deal with increment 7',
    'cut 8',
    'cut -4',
    'deal with increment 7',
    'cut 3',
    'deal with increment 9',
    'deal with increment 3',
    'cut -1'
]))


#print(solve1(10, ['deal with increment 3']))


#print('Part 1 ', solve1(10007, data).index(2019))
#print('Part 2 ', solve1(119315717514047, data).index(2020))
#print('Part 2 ', solve2(data))
#print(119315717514047)
############1000000000
#print(isprime(119315717514047))
#print(101741582076661)
#print(isprime(101741582076661))
#print(igcd(119315717514047, 101741582076661))

#print(solve1(10007, data).index(2020))
#print(solve1(nextprime(10007, 1), data).index(2020))
#print(solve1(nextprime(10007, 2), data).index(2020))
#print(solve1(nextprime(10007, 4), data).index(2020))
#print(solve1(nextprime(10007, 10), data).index(2020))
#print(solve1(nextprime(10007, 3), data).index(2020))
#print(solve1(nextprime(10007, 100), data).index(2020))
#print(solve1(nextprime(10007, 100), data).index(2020))
#print(solve1(nextprime(2020, 1), data).index(2020))

original_deck = list(range(0, 10007))
new_deck = original_deck.copy()
count = 0

while True:
    count += 1
    new_deck = solve1(10007, data, new_deck)
    if original_deck == new_deck:
        print(count)
        break
    if count % 100 == 0:
        print(count)
        print(new_deck.index(2020))

quit()

prime = 10009
while True:
    print(f'{prime}: ', solve1(prime, data).index(2020))
    answer = solve1(prime, data).index(2020)
    prime = nextprime(prime)
    if answer == 2575:
        break

#print('2021 ', solve1(int(10007 * 2), data).index(2020))
#print('4040 ', solve1(10009, data).index(2020))
print(nextprime(119315717514047))
