#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from itertools import permutations

test_input="""swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 steps
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

class Scrambler(object):
    def __init__(self, inputs):
        self.rules = []
        self.password = []
        re_swap_position = re.compile("swap position ([0-9]+) with position ([0-9]+)")
        re_swap_letter = re.compile("swap letter ([a-z]) with letter ([a-z])")
        re_rotate_steps = re.compile("rotate (left|right) ([0-9]+) steps?")
        re_rotate_letter = re.compile("rotate based on position of letter ([a-z])")
        re_reverse = re.compile("reverse positions ([0-9]+) through ([0-9]+)")
        re_move_position = re.compile("move position ([0-9]+) to position ([0-9]+)")
        
        for line in inputs:
            line = line.strip()
            if len(line) == 0:
                continue
            m = re_swap_position.match(line)
            if m:
                self.rules.append((Scrambler.do_swap_position, tuple(map(int, m.groups())) ))
                continue
            m = re_swap_letter.match(line)
            if m:
                self.rules.append((Scrambler.do_swap_letter, m.groups()))
                continue
            m = re_rotate_steps.match(line)
            if m:
                self.rules.append((Scrambler.do_rotate_steps, (m.group(1), int(m.group(2))) ))
                continue
            m = re_rotate_letter.match(line)
            if m:
                self.rules.append((Scrambler.do_rotate_letter, m.groups()))
                continue
            m = re_reverse.match(line)
            if m:
                self.rules.append((Scrambler.do_reverse_positions, tuple(map(int, m.groups())) ))
                continue
            m = re_move_position.match(line)
            if m:
                self.rules.append((Scrambler.do_move_position, tuple(map(int, m.groups())) ))
                continue
            raise Exception(line)
    
    def do_swap_position(self, a, b):
        self.password[a], self.password[b] = self.password[b], self.password[a]
    def do_swap_letter(self, l1, l2):
        a = self.password.index(l1)
        b = self.password.index(l2)
        self.password[a], self.password[b] = self.password[b], self.password[a]
    def do_rotate_steps(self, direction, n):
        if direction == "left":
            self.password = self.password[n:] + self.password[:n]
        else:
            self.password = self.password[-n:] + self.password[:-n]
    def do_rotate_letter(self, l):
        a = self.password.index(l)
        self.password = self.password[-1:] + self.password[:-1]
        self.password = self.password[-a:] + self.password[:-a]
        if a >= 4:
            self.password = self.password[-1:] + self.password[:-1]
    def do_reverse_positions(self, a, b):
        self.password = self.password[0:a] + list(reversed(self.password[a:b+1])) + self.password[b+1:]
    def do_move_position(self, a, b):
        t = self.password[a]
        del self.password[a]
        self.password.insert(b, t)
        
    
    def run(self, password):
        self.password = list(password)
        for rule in self.rules:
            rule[0](self, *rule[1])
        return "".join(self.password)

            
def work_p1(inputs, password):
    scrambler = Scrambler(inputs)
    p = scrambler.run(password)
    return p

def work_p2(inputs, password):
    scrambler = Scrambler(inputs)
    for p in permutations(password, len(password)):
        r = scrambler.run(p)
        if r == password:
            return "".join(p)

def test_p1():
    assert(work_p1(test_input, "abcde") == "decab")
test_p1()

def p1():
    print(work_p1(fileinput.input(), "abcdefgh"))
p1()

def p2():
    print(work_p2(fileinput.input(), "fbgdceah"))
p2()
