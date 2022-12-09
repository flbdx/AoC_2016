#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

def TLS_support(ip):
    ip = ip.replace(']', ' [') # yup
    parts = ip.split('[') # yup
    abba_outside_bracket = False
    abba_inside_bracket = False
    
    def find_abba(s):
        for i in range(0, len(s) - 3):
            if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
                return True
        return False
    
    for part in parts:
        brackets = (part[-1] == ' ') # yup...
        if brackets:
            abba_inside_bracket |= find_abba(part)
        else:
            abba_outside_bracket |= find_abba(part)
            
    if abba_inside_bracket:
        return False
    return abba_outside_bracket

def SSL_support(ip):
    ip = ip.replace(']', ' [') # -_-
    parts = ip.split('[')
    all_ABAs = set()
    all_BABs = set()
    
    def find_all_XYX(s):
        l = []
        for i in range(0, len(s) - 2):
            if s[i] == s[i+2] and s[i] != s[i+1]:
                l.append(s[i:i+3])
        return l
    
    for part in parts:
        brackets = (part[-1] == ' ')
        if brackets:
            all_BABs.update(find_all_XYX(part))
        else:
            all_ABAs.update(find_all_XYX(part))
    
    for aba in all_ABAs:
        if aba[1]+aba[0]+aba[1] in all_BABs:
            return True
    return False

def work_p1(lines):
    ret = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if TLS_support(line):
            ret += 1
    return ret

def work_p2(lines):
    ret = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if SSL_support(line):
            ret += 1
    return ret

def test_p1():
    assert(TLS_support("abba[mnop]qrst") == True)
    assert(TLS_support("abcd[bddb]xyyx") == False)
    assert(TLS_support("aaaa[qwer]tyui") == False)
    assert(TLS_support("ioxxoj[asdfgh]zxcvbn") == True)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p1():
    assert(SSL_support("aba[bab]xyz") == True)
    assert(SSL_support("xyx[xyx]xyx") == False)
    assert(SSL_support("aaa[kek]eke") == True)
    assert(SSL_support("zazbz[bzb]cdb") == True)
test_p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
