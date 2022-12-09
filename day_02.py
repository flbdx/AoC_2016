#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

sample_input = """ULL
RRDDD
LURDL
UUUUD"""

moves = {'U': complex(0, 1),
         'D': complex(0, -1),
         'L': complex(-1, 0),
         'R': complex(1, 0)}

numbers = {complex(0, 2): '1', complex(1, 2): '2', complex(2, 2): '3',
           complex(0, 1): '4', complex(1, 1): '5', complex(2, 1): '6',
           complex(0, 0): '7', complex(1, 0): '8', complex(2, 0): '9'}

nightmare = {
                                             complex(2, 4): '1',
                         complex(1, 3): '2', complex(2, 3): '3', complex(3, 3): '4',
     complex(0, 2): '5', complex(1, 2): '6', complex(2, 2): '7', complex(3, 2): '8', complex(4, 2): '9',
                         complex(1, 1): 'A', complex(2, 1): 'B', complex(3, 1): 'C',
                                             complex(2, 0): 'D'
    }

def work_p1(lines, keypad):
    p = complex(1, 1)
    s = ""
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        for c in line:
            p2 = p + moves[c]
            if not p2 in keypad.keys():
                continue
            p = p2
        s += keypad.get(p)
    return s

def test_p1():
    assert work_p1(sample_input.splitlines(), numbers) == "1985"
test_p1()

def p1():
    print(work_p1(fileinput.input(), numbers))
p1()

def test_p2():
    assert work_p1(sample_input.splitlines(), nightmare) == "5DB3"
test_p2()

def p2():
    print(work_p1(fileinput.input(), nightmare))
p2()

