#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from itertools import combinations
from collections import deque

test_input="""The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".splitlines()

def read_input(inputs, part2=False):
    lines = list(inputs)
    elements = {}
    if part2:
        elements["elerium"] = 0
        elements["dilithium"] = 0
    
    # discover the elements and assign an index to each of them
    for floor in range(4):
        line = lines[floor].strip()
        words = line.split(" ")
        for i in range(len(words) - 1):
            if words[i+1].startswith("microchip"):
                element = words[i].split("-")[0]
                if not element in elements:
                    elements[element] = len(elements)
    
    # now build the state
    # first len(elements) bytes are the generator's floors
    # next len(elements) bytes are the microchip's floors
    # the last byte is the elevator's floor
    state = bytearray([0]*(2*len(elements) + 1))
    for floor in range(4):
        line = lines[floor].strip()
        words = line.split(" ")
        for i in range(len(words) - 1):
            if words[i+1].startswith("microchip"):
                element = words[i].split("-")[0]
                element = elements[element]
                state[element + len(elements)] = floor
            elif words[i+1].startswith("generator"):
                element = words[i]
                element = elements[element]
                state[element] = floor
    
    #print(elements)
    return bytes(state), len(elements)

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

# check that nothing's burning
def state_is_valid(state, n_elements):
    for e in range(n_elements):
        if state[e] == state[e+n_elements]:
            # this element is shielded
            continue
        floor = state[e+n_elements] # this microchip's floor
        for e2 in range(n_elements):
            if state[e2] == floor: # enerator on the same floor
                return False
    return True

# returns all the valid next states from the given state
# possible_next_states.permut_2 is a cache for list(combinations(range(2*n_elements), 2)
def possible_next_states(state, n_elements):
    l = []
    floor = state[2*n_elements]
    for direction in (-1, 1): #going down or up
        if floor == 0 and direction == -1:
            continue
        if floor == 3 and direction == 1:
            continue
        nstate = bytearray(state)
        nstate[2*n_elements] += direction
        for x in range(2*n_elements): # moving one chip/gen
            if state[x] == floor:
                nstate[x] += direction
                if state_is_valid(nstate, n_elements):
                    l.append(bytes(nstate))
                nstate[x] -= direction
        for x, y in possible_next_states.permut_2.setdefault(n_elements, list(combinations(range(2*n_elements), 2))): # moving two chips/gens
            if state[x] == floor and state[y] == floor:
                nstate[x] += direction
                nstate[y] += direction
                if state_is_valid(nstate, n_elements):
                    l.append(bytes(nstate))
                nstate[x] -= direction
                nstate[y] -= direction
    return l
possible_next_states.permut_2 = {}

# First part : simple BFS search, pretty fast
def work_p1(inputs):
    state, n_elements = read_input(inputs)
    
    start_state = state
    final_state = bytes([3]*len(state))
    
    seen_states = set()
    q = deque()
    q.appendleft((start_state, 0))
    seen_states.add(start_state)
    while len(q) != 0:
        state, d = q.popleft()
        if state == final_state:
            return d
        for nxt in possible_next_states(state, n_elements):
            if not nxt in seen_states:# or (seen_states[nxt] > d+1):
                q.append((nxt, d+1))
                seen_states.add(nxt)

# 2nd part, the state is 256x large
# Use a "meet in the midle" double BFS
# It's still quite slow
def work_p2(inputs):
    state, n_elements = read_input(inputs, part2=True)
    
    start_state = state
    final_state = bytes([3]*len(state))
    
    #print(start_state, final_state)
    
    seen_states_start = {}
    seen_states_final = {}
    q_start = deque()
    q_final = deque()
    q_start.appendleft((start_state, 0))
    seen_states_start[start_state] = 0
    q_final.appendleft((final_state, 0))
    seen_states_final[final_state] = 0
    
    while True:
        next_q_start = deque()
        next_q_final = deque()
        while len(q_start) != 0:
            state, d = q_start.popleft()
            if state == final_state:
                return d
            if state in seen_states_final:
                return d + seen_states_final[state]
            for nxt in possible_next_states(state, n_elements):
                if not nxt in seen_states_start:
                    next_q_start.append((nxt, d+1))
                    seen_states_start[nxt] = d+1
        q_start = next_q_start
        
        while len(q_final) != 0:
            state, d = q_final.popleft()
            if state == start_state:
                return d
            if state in seen_states_start:
                return d + seen_states_start[state]
            for nxt in possible_next_states(state, n_elements):
                if not nxt in seen_states_final:
                    next_q_final.append((nxt, d+1))
                    seen_states_final[nxt] = d+1
        q_final = next_q_final

def test_p1():
    assert(work_p1(test_input) == 11)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
