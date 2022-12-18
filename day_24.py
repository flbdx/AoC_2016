#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import networkx as nx
from enum import Enum
from itertools import combinations
from collections import deque, namedtuple

test_input="""###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

def parse_input(inputs):
    world = {}
    locations = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            if c.isnumeric():
                locations[int(c)] = (x,y)
            world[(x,y)] = c
    return world, locations

class Direction(Enum):
    UP = ord('^')
    DOWN = ord('v')
    LEFT = ord('<')
    RIGHT = ord('>')
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

def work_p1_p2(inputs, part2 = False):
    world, locations = parse_input(inputs)
    
    G = nx.Graph()
    for p, c in world.items():
        if c == '#':
            continue
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            n = direction.next(p)
            if world.get(n, '#') != '#':
                G.add_edge(p, n)
                
    location_names = list(locations.keys())
    best_distances = {}
    for a, b in combinations(location_names, 2):
        pa, pb = locations[a], locations[b]
        d = nx.shortest_path_length(G, pa, pb)
        best_distances[a] = best_distances.get(a, {}) | {b: d}
        best_distances[b] = best_distances.get(b, {}) | {a: d}
        
    best_path = None
    best_d = None
    stack = deque()
    State = namedtuple("State", ["path", "to_visit", "distance"])
    stack.append(State([0], [n for n in location_names if n != 0], 0))
    while len(stack) != 0:
        state = stack.pop()
        if len(state.to_visit) == 0:
            d = (state.distance + best_distances[state.path[-1]][0]) if part2 else state.distance
            p = (state.path + [0]) if part2 else state.path
            if best_d == None or d < best_d:
                best_d = d
                best_path = p
            continue
        
        for i in range(len(state.to_visit)):
            nxt = state.to_visit[i]
            stack.append(State(state.path + [nxt], state.to_visit[0:i] + state.to_visit[i+1:], state.distance + best_distances[state.path[-1]][nxt]))
    
    print(best_path)
    return best_d

def test_p1():
    assert(work_p1_p2(test_input) == 14)
test_p1()

def p1():
    print(work_p1_p2(fileinput.input()))
p1()

def p2():
    print(work_p1_p2(fileinput.input(), True))
p2()
