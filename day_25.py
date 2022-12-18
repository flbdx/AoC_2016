#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

class VM(object):
    def __init__(self, assembunny):
        self.instructions = []
        self.reset()
        
        for line in assembunny:
            line = line.strip()
            if len(line) == 0:
                continue
            words = line.split(" ")
            
            if words[0] == "cpy":
                self.instructions.append((getattr(VM, "do_cpy"), words[1:]))
            elif words[0] == "inc":
                self.instructions.append((getattr(VM, "do_inc"), words[1:]))
            elif words[0] == "dec":
                self.instructions.append((getattr(VM, "do_dec"), words[1:]))
            elif words[0] == "jnz":
                self.instructions.append((getattr(VM, "do_jnz"), words[1:]))
            elif words[0] == "out":
                self.instructions.append((getattr(VM, "do_out"), words[1:]))
    
    def reset(self):
        self.ip = 0
        self.regs = {n:0 for n in "abcd"}
    
    def run_one(self):
        instr, ops = self.instructions[self.ip]
        self.ip += instr(self, *ops)
        return (self.ip, self.ip < 0 or self.ip >= len(self.instructions))
    
    def do_cpy(self, x, y):
        print("{ip: >2}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, instr="cpy", r1=x, r2=y, regs=self.regs))
        self.regs[y] = self.regs[x] if x in "abcd" else int(x)
        return 1
    
    def do_inc(self, x):
        print("{ip: >2}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, instr="inc", r1=x, r2=" ", regs=self.regs))
        self.regs[x] += 1
        return 1
    
    def do_dec(self, x):
        print("{ip: >2}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, instr="dec", r1=x, r2=" ", regs=self.regs))
        self.regs[x] -= 1
        return 1
    
    def do_jnz(self, x, y):
        print("{ip: >2}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, instr="jnz", r1=x, r2=y, regs=self.regs))
        x = self.regs[x] if x in "abcd" else int(x)
        y = self.regs[y] if y in "abcd" else int(y)
        return y if x != 0 else 1
    
    def do_out(self, x):
        print("{ip: >2}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, instr="out", r1=x, r2=" ", regs=self.regs))
        x = self.regs[x] if x in "abcd" else int(x)
        return 1


def work_p1(inputs):
    # for my input, we have a = a + 170*15
    # then it will repeatdly output a binary decomposition of a, starting from the LSB
    # it takes "a few" instructions...
    
    import math
    n = 170*15
    n2 = math.log(n, 2)
    n2 = int(math.ceil(n2))
    assert((n2&0) == 0) # number of bits is even
    ret = 0 # generate a long enough 101010 pattern
    for i in range(n2//2):
        ret = (ret << 2) | 0b10
    return ret - n
    
#     vm = VM(inputs)
#     
#     vm.regs["a"] = 180
#     
#     # for i in range(2000):
#     while True:
#         ip, terminated = vm.run_one()
#         if terminated:
#             break
#     # return vm.regs["a"]

def p1():
    print(work_p1(fileinput.input()))
p1()
