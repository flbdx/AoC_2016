#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

class Elf(object):
    def __init__(self, n):
        self.prev = None
        self.next = None
        self.n = n
    def detach(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = None
        self.next = None
    def alone(self):
        return self == self.prev
    
    def __repr__(self):
        return repr(self.n)

def build_circle(n_elfs):
    elfs = []
    for i in range(n_elfs):
        e = Elf(i+1)
        if len(elfs) == 0:
            elfs.append(e)
        else:
            e.prev = elfs[-1]
            elfs[-1].next = e
            elfs.append(e)
    elfs[0].prev = elfs[-1]
    elfs[-1].next = elfs[0]
    return elfs

def work_p1(n_elfs):
    elfs = build_circle(n_elfs)
    
    e = elfs[0]
    while True:
        if not e.alone():
            e.next.detach()
            e = e.next
        else:
            break
    return e.n

def work_p2(n_elfs):
    elfs = build_circle(n_elfs)
    
    e = elfs[0]
    op = elfs[n_elfs//2] # opposite elf
    
    while True:
        if not e.alone():
            next_op = op.next if (n_elfs & 1) == 0 else op.next.next
            op.detach()
            n_elfs -= 1
            e = e.next
            op = next_op
        else:
            break
    return e.n

def test_p1():
    assert(work_p1(5) == 3)
test_p1()

def p1():
    print(work_p1(3012210))
p1()

def test_p2():
    assert(work_p2(5) == 2)
test_p2()

def p2():
    print(work_p2(3012210))
p2()
