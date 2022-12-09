#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

sample_input = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

def work(lines, part2=False):
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if len(l) != 0]
    nl = len(lines)
    w = len(lines[0])
    ret = ""
    for i in range(w):
        cpt = {}
        for l in range(nl):
            cpt[lines[l][i]] = cpt.get(lines[l][i], 0) + 1
        if not part2:
            ret += sorted(cpt.keys(), key=lambda x: -cpt[x])[0]
        else:
            ret += sorted(cpt.keys(), key=lambda x: cpt[x])[0]
    return ret


def test_p1():
    assert(work(sample_input.splitlines()) == "easter")
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def test_p2():
    assert(work(sample_input.splitlines(), part2=True) == "advent")
test_p2()

def p1():
    print(work(fileinput.input(), part2=True))
p1()
