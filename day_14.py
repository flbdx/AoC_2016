#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque
import hashlib
#from Crypto.Hash import MD5 # it's worse ...

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

test_input="""abc"""
real_input = next(fileinput.input()).strip()

def simple_hash(s):
    return hashlib.md5(s.encode("ASCII")).hexdigest()
def stretched_hash(s):
    h = hashlib.md5(s.encode("ASCII")).hexdigest()
    for i in range(2016):
        h = hashlib.md5(h.encode("ASCII")).hexdigest()
    return h

def work(salt, hash_func):
    n_keys = 0
    idx = 0
    q = deque()
    for i in range(1001):
        h = hash_func(salt + repr(idx + i))
        q.append(h)
    
    def is_key():
        nonlocal q
        h = q[0]
        for i in range(0, 32-2):
            if h[i] == h[i + 1] and h[i] == h[i + 2]:
                s = h[i] * 5
                it = iter(q)
                next(it)
                for h2 in it:
                    if s in h2:
                        return True
                return False
        return False
        
    
    while True:
        if is_key():
            #print(idx, q[0])
            n_keys += 1
            if n_keys == 64:
                break
        idx += 1
        q.popleft()
        q.append(hash_func(salt + repr(idx + 1000)))
    return idx
    

def work_p2(inputs):
    pass

def test_p1():
    assert(work(test_input, simple_hash) == 22728)
test_p1()

def p1():
    print(work(real_input, simple_hash))
p1()

def test_p2():
    assert(work(test_input, stretched_hash) == 22551)
test_p2()

def p2():
    print(work(real_input, stretched_hash))
p2()
