#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from hashlib import md5
from collections import deque

real_input = "gdjjyniy"

class Direction(Enum):
    U = complex(0, -1)
    D = complex(0, 1)
    L = complex(-1, 0)
    R = complex(1, 0)

# precompute all the directions from the first 2 bytes of a hash
int_to_dirs = {}
for n in range(1<<16):
    l = []
    if (n & 0xF) >= 11:
        l.append((Direction.R, b'R'))
    if ((n >> 4) & 0xF) >= 11:
        l.append((Direction.L, b'L'))
    if ((n >> 8) & 0xF) >= 11:
        l.append((Direction.D, b'D'))
    if ((n >> 12) & 0xF) >= 11:
        l.append((Direction.U, b'U'))
    int_to_dirs[n] = l

# salt + path -> list of directions and direction's letters
def path_to_dirs(salt, path):
    h = md5(salt + path).digest()
    return int_to_dirs[int.from_bytes(h[:2], "big", signed=False)]
        
def work(inputs, part2=False):
    salt = inputs.strip().encode("ASCII")
    
    q = deque()
    start = complex(0, 0)
    end = complex(3, 3)
    q.append((start, b""))
    
    max_path_len = 0 # for part 2
    
    while len(q) > 0:
        pos, path = q.popleft()
        for dir, dir_name in path_to_dirs(salt, path):
            npos = pos + dir.value
            if npos.real < 0 or npos.real > 3 or npos.imag < 0 or npos.imag > 3:
                continue
            if npos == end:
                if part2:
                    max_path_len = max(max_path_len, len(path) + 1)
                else:
                    # for part 1, returns the 1st valid paths
                    return path + dir_name
            else:
                q.append((npos, path + dir_name))    
    
    # part2
    return max_path_len

def work_p2(inputs):
    pass

def test_p1():
    assert(work("ihgpwlah") == b"DDRRRD")
    assert(work("kglvqrro") == b"DDUDRLRRUDRD")
    assert(work("ulqzkmiv") == b"DRURDRUDDLLDLUURRDULRLDUUDDDRR")
test_p1()

def p1():
    print(work(real_input))
p1()

def test_p2():
    assert(work("ihgpwlah", True) == 370)
    assert(work("kglvqrro", True) == 492)
    assert(work("ulqzkmiv", True) == 830)
test_p2()

def p2():
    print(work(real_input, True))
p2()
