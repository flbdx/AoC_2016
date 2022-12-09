#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input="""Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

def read_input(inputs):
    discs = {}
    re_int = re.compile("[0-9]+")
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        ints = list(map(int, re_int.findall(line)))
        discs[ints[0]] = (ints[1], ints[3])
    return discs
        
# the inputs are small enough for a bruteforce search

#def work(inputs, part2=False):
    #discs = read_input(inputs)
    #if part2:
        #discs[len(discs) + 1] = (11,0)
    ##print(discs)
    
    #def can_passthrough(release_time, disc_n):
        #disc_p = (release_time + disc_n + discs[disc_n][1]) % discs[disc_n][0]
        #return disc_p == 0
    
    #t = 1
    #while True:
        #ok = True
        #for disc_n in discs:
            #if not can_passthrough(t, disc_n):
                #ok = False
                #break
        #if ok:
            #return t
        #t += 1

def work_crt(inputs, part2=False):
    discs = read_input(inputs)
    if part2:
        discs[len(discs) + 1] = (11,0)
        
    # for each disc with NP positions, delay D and start position S :
    # we are searching the release time t such as
    # (t + D + S) == 0 mod NP
    # therefore
    # t mod NP == (-t-S) mod NP
    #
    # moreover we can check that every NP is prime
    # so we can use the chinese remainder theorem to find
    # t mod (NP_1 * NP_2 * ... NP_n)
    # wich will be the first time where all discs are aligned
    
    period = 1
    for disc in discs:
        period *= discs[disc][0]
    
    # direct from https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_restes_chinois#Algorithme
    t = 0
    for disc in discs:
        ni = discs[disc][0]
        ai = (-(disc + discs[disc][1])) % ni
        
        n_ni = period // ni
        inv_n_ni = pow(n_ni, ni-2, ni)
        ei = inv_n_ni * n_ni
        t += ai * ei
    return (t % period)

def test_p1():
    #assert(work(test_input) == 5)
    assert(work_crt(test_input) == 5)
test_p1()

def p1():
    #print(work(fileinput.input()))
    print(work_crt(fileinput.input()))
p1()

def p2():
    #print(work(fileinput.input(), True))
    print(work_crt(fileinput.input(), True))
p2()
