#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

def work_p1(lines):
    re_int = re.compile("[-]?[0-9]+")
    valids = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        ints = list(map(int, re_int.findall(line)))
        
        ints = sorted(ints)
        if ints[0] + ints[1] > ints[2]:
            valids += 1
    return valids

def work_p2(lines):
    re_int = re.compile("[-]?[0-9]+")
    valids = 0
    all_ints = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        all_ints.append(list(map(int, re_int.findall(line))))

    for i in range(0, len(all_ints), 3):
        for j in range(0, 3):
            ints = [all_ints[i][j], all_ints[i+1][j], all_ints[i+2][j]]
            ints = sorted(ints)
            if ints[0] + ints[1] > ints[2]:
                valids += 1

    return valids

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()

