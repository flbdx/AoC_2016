#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input=""".^^.^.^^^^""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

def read_input(inputs):
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        row = tuple(1 if c == '^' else 0 for c in line)
    return row
    
def work(inputs, n_rows):
    row = read_input(inputs)
    w = len(row)
    def gen(col):
        if col == 0:
            return row[col+1]
        if col == w-1:
            return row[col-1]
        # return row[col-1] ^ row[col+1] # slower
        return 1 if row[col-1] != row[col+1] else 0
    
    n_traps = sum(row)
    for r in range(1, n_rows):
        new_row = tuple(gen(c) for c in range(0, w))
        n_traps += sum(new_row)
        row = new_row
    
    # complements to get the number of safe tiles
    return w * n_rows - n_traps

def test_p1():
    assert(work(test_input, n_rows=10) == 38)
test_p1()

def p1():
    print(work(fileinput.input(), n_rows=40))
p1()

def p2():
    print(work(fileinput.input(), n_rows=400000))
p2()
