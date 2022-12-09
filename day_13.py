#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque
import functools

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

test_input=10
real_input=int(next(fileinput.input()))

class Grid(object):
    def __init__(self, fav):
        self.fav = fav
    
    @functools.cache
    def __getitem__(self, key):
        try:
            x, y = key[0], key[1]
            v = x*x + 3*x + 2*x*y + y + y*y
            v += self.fav
            #bitcnt = sum(1 for c in bin(v) if c == '1')
            bitcnt = 0
            while v != 0:
                if v & 1:
                    bitcnt += 1
                v //= 2
            return 1 if (bitcnt&1) else 0
        except:
            pass
        raise KeyError

def neighbours(n):
    x, y = n[0], n[1]
    l = [(x+1, y), (x, y+1)]
    if x > 0:
        l.append((x-1, y))
    if y > 0:
        l.append((x, y-1))
    return l

def work_p1(inputs, dest_node=(31,39)):
    g = Grid(inputs)
        
    start_node = (1,1)
    q = deque()
    seen_nodes = {start_node:0}
    q.appendleft((start_node, 0))
    
    while len(q) != 0:
        node, d = q.popleft()
        if node == dest_node:
            return d
        nd = d+1
        for nxt in neighbours(node):
            if g[nxt] == 1:
                continue
            if not nxt in seen_nodes or seen_nodes[nxt] > nd:
                q.append((nxt, nd))
                seen_nodes[nxt] = nd

def work_p2(inputs, max_d=50):
    g = Grid(inputs)
        
    start_node = (1,1)
    q = deque()
    seen_nodes = {start_node:0}
    for d in range(max_d):
        q = deque(n for n,nd in seen_nodes.items() if nd == d)
        while len(q) != 0:
            node = q.popleft()
            for nxt in neighbours(node):
                if g[nxt] == 1:
                    continue
                if not nxt in seen_nodes or seen_nodes[nxt] > d+1:
                    seen_nodes[nxt] = d+1
    return len(seen_nodes)
    

def test_p1():
    assert(work_p1(test_input, (7,4)) == 11)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def p2():
    print(work_p2(real_input))
p2()
