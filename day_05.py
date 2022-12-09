#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import hashlib # it's going to be slow...

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

sample_input = """abc"""

def work_p1(door_id, pwd_len = 8):
    i = 0
    l = 0
    pwd = ""
    while l != pwd_len:
        s = door_id + repr(i)
        h = hashlib.md5(s.encode("ASCII")).hexdigest()
        if h.startswith("00000"):
            pwd += h[5]
            l += 1
        i += 1
    return pwd

def work_p2(door_id, pwd_len = 8):
    i = 0
    filed_positions = set()
    pwd = ["_"] * pwd_len
    while len(filed_positions) != pwd_len:
        s = door_id + repr(i)
        h = hashlib.md5(s.encode("ASCII")).hexdigest()
        if h.startswith("00000"):
            p = int(h[5], 16)
            if p < pwd_len and not p in filed_positions:
                pwd[p] = h[6]
                filed_positions.add(p)
        i += 1
    return "".join(pwd)

def test_p1():
    assert(work_p1(sample_input) == "18f47a30")
test_p1()

def p1():
    lines = list(fileinput.input())
    print(work_p1(lines[0].strip()))
p1()

def test_p2():
    assert(work_p2(sample_input) == "05ace8e3")
test_p2()

def p2():
    lines = list(fileinput.input())
    print(work_p2(lines[0].strip()))
p2()
