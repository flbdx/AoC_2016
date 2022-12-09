#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_09"]
    
def work(line, part2=False):
    idx1 = line.find('(')
    if idx1 == -1:
        return len(line)
    idxx = line.find('x', idx1+1)
    idx2 = line.find(')', idxx+1)
    i1 = int(line[idx1+1:idxx])
    i2 = int(line[idxx+1:idx2])
    if part2:
        # let's assume that a compressed part doesn't overlap with the next data
        return idx1 + (work(line[idx2+1:idx2+1+i1], True) * i2) + work(line[idx2+1+i1:], True)
    else:
        return idx1 + (i1 * i2) + work(line[idx2+1+i1:])

def test_p1():
    assert(work("ADVENT") == len("ADVENT"))
    assert(work("A(1x5)BC") == len("ABBBBBC"))
    assert(work("(3x3)XYZ") == len("XYZXYZXYZ"))
    assert(work("A(2x2)BCD(2x2)EFG") == len("ABCBCDEFEFG"))
    assert(work("(6x1)(1x3)A") == len("(1x3)A"))
    assert(work("X(8x2)(3x3)ABCY") == len("X(3x3)ABC(3x3)ABCY"))
test_p1()

def p1():
    print(work(list(fileinput.input())[0].strip()))
p1()

def test_p2():
    assert(work("(3x3)XYZ", True) == len("XYZXYZXYZ"))
    assert(work("X(8x2)(3x3)ABCY", True) == len("XABCABCABCABCABCABCY"))
    assert(work("(27x12)(20x12)(13x14)(7x10)(1x12)A", True) == 241920)
    assert(work("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", True) == 445)
test_p2()

def p2():
    print(work(list(fileinput.input())[0].strip(), True))
p2()
