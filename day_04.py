#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

sample_input = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

def parse_room(line):
    i = line.rindex("-")
    name = line[:i]
    l = line[i+1:-1].split('[')
    sector_id, checksum = l
    sector_id = int(sector_id)
    
    return (name, sector_id, checksum)

def room_is_real(name, checksum):
    letters = {}
    for l in name:
        if l != '-':
            letters[l] = letters.get(l, 0) + 1
    ck = "".join(sorted(letters.keys(), key=lambda l: (-letters[l], l)))
    if len(ck) > 5:
        ck = ck[:5]
    return checksum == ck

def work_p1(lines):
    ret = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        n, s, c = parse_room(line)
        
        if room_is_real(n, c):
            ret += s
    return ret

def work_p2(lines):
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        n, s, c = parse_room(line)
        
        ord_a = ord('a')
        if room_is_real(n, c):
            decrypted = ""
            for l in n:
                if l == '-':
                    decrypted += ' '
                else:
                    decrypted += chr(((ord(l) - ord_a + s) % 26) + ord_a)
            if "north" in decrypted:
                return s
    
    

def test_p1():
    assert(work_p1(sample_input.splitlines()) == 1514)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
