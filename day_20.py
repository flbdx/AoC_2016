#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""5-8
0-2
4-7""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

def read_input(inputs):
    ranges = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        rng = tuple(int(v) for v in line.split("-"))
        ranges.append(rng)
    return ranges

def fuse_ranges(ranges):
    rng_it = iter(sorted(ranges))
    fused_ranges = [next(rng_it)]
    for rng in rng_it:
        if rng[0] <= fused_ranges[-1][1] + 1:
            fused_ranges[-1] = (fused_ranges[-1][0], max(fused_ranges[-1][1], rng[1]))
        else:
            fused_ranges.append(rng)
    return fused_ranges

def work_p1(inputs):
    ranges = read_input(inputs)
    fused_ranges = fuse_ranges(ranges)
    first = fused_ranges[0]
    if first[0] == 0:
        return first[1] + 1
    else:
        return 0

def work_p2(inputs, max_ip):
    ranges = read_input(inputs)
    fused_ranges = fuse_ranges(ranges)
    
    valid_ips = 0
    prev = -1
    for ban in fused_ranges:
        valid_ips += ban[0] - prev - 1
        prev = ban[1]
    valid_ips += max_ip - prev
    return valid_ips

def test_p1():
    assert(work_p1(test_input) == 3)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input, 9) == 2)
test_p2()

def p2():
    print(work_p2(fileinput.input(), 4294967295))
p2()
