#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

def work_p1(lines):
    p = complex(0, 0)
    d = complex(0, 1)
    line = list(lines)[0].strip()
    for instr in line.split(", "):
        r = instr[0]
        l = int(instr[1:])
        if r == 'R':
            d *= -1j
        else:
            d *= +1j
        p += d * l
    
    return abs(p.real) + abs(p.imag)

def work_p2(lines):
    p = complex(0, 0)
    d = complex(0, 1)
    visited = {p}
    line = list(lines)[0].strip()
    for instr in line.split(", "):
        r = instr[0]
        l = int(instr[1:])
        if r == 'R':
            d *= -1j
        else:
            d *= +1j
        found = False
        for i in range(l):
            p += d 
            if p in visited:
                found = True
                break
            visited.add(p)
        if found:
            break
    return abs(p.real) + abs(p.imag)

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert work_p2(["R8, R4, R4, R8"]) == 4
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
