#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

class VM(object):
    def __init__(self, assembunny):
        self.instructions = []
        self.toggled = {}
        self.reset()
        
        for line in assembunny:
            line = line.strip()
            if len(line) == 0:
                continue
            words = line.split(" ")
            
            if words[0] == "cpy":
                self.instructions.append((getattr(VM, "do_cpy"), getattr(VM, "do_jnz"), words[1:]))
            elif words[0] == "inc":
                self.instructions.append((getattr(VM, "do_inc"), getattr(VM, "do_dec"), words[1:]))
            elif words[0] == "dec":
                self.instructions.append((getattr(VM, "do_dec"), getattr(VM, "do_inc"), words[1:]))
            elif words[0] == "jnz":
                self.instructions.append((getattr(VM, "do_jnz"), getattr(VM, "do_cpy"), words[1:]))
            elif words[0] == "tgl":
                self.instructions.append((getattr(VM, "do_tgl"), getattr(VM, "do_inc"), words[1:]))
    
    def reset(self):
        self.ip = 0
        self.regs = {n:0 for n in "abcd"}
    
    def run_one(self):
        instr1, instr2, ops = self.instructions[self.ip]
        if self.toggled.get(self.ip, False):
            try:
                self.ip += instr2(self, *ops)
            except:
                self.ip += 1
        else:
            self.ip += instr1(self, *ops)
        return (self.ip, self.ip < 0 or self.ip >= len(self.instructions))
    
    def do_cpy(self, x, y):
        # print("{ip: >2} {toggled: <1}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, toggled=self.toggled.get(self.ip, False), instr="cpy", r1=x, r2=y, regs=self.regs))
        self.regs[y] = self.regs[x] if x in "abcd" else int(x)
        return 1
    
    def do_inc(self, x):
        # print("{ip: >2} {toggled: <1}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, toggled=self.toggled.get(self.ip, False), instr="inc", r1=x, r2=" ", regs=self.regs))
        self.regs[x] += 1
        return 1
    
    def do_dec(self, x):
        # print("{ip: >2} {toggled: <1}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, toggled=self.toggled.get(self.ip, False), instr="dec", r1=x, r2=" ", regs=self.regs))
        self.regs[x] -= 1
        return 1
    
    def do_jnz(self, x, y):
        # print("{ip: >2} {toggled: <1}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, toggled=self.toggled.get(self.ip, False), instr="jnz", r1=x, r2=y, regs=self.regs))
        x = self.regs[x] if x in "abcd" else int(x)
        y = self.regs[y] if y in "abcd" else int(y)
        return y if x != 0 else 1

    def do_tgl(self, x):
        # print("{ip: >2} {toggled: <1}    {instr} {r1: <2} {r2: <2}    {regs}".format(ip=self.ip, toggled=self.toggled.get(self.ip, False), instr="tgl", r1=x, r2=" ", regs=self.regs))
        x = self.regs[x] if x in "abcd" else int(x)
        self.toggled[self.ip + x] = True
        return 1
            

def work_p1(inputs):
    vm = VM(inputs)
    
    vm.regs["a"] = 7
    
    while True:
        ip, terminated = vm.run_one()
        if terminated:
            break
    return vm.regs["a"]
    

def work_p2(inputs, test=False):
    # the input assembunny code is quite fun!
    
    # a first loop compute a = a*b
    # it is used to compute a*(a-1)*(a-2)*..*2
    # after each multiplication an instruction is toggled
    # after the last multiplication, the jump is toggled to continue to the 2nd part
    # the 2nd part will add 75*72 to the result

    a = 7 if test else 12
    r = 1
    while a != 1:
        r *= a
        a -= 1
    r += 75*72
    return r

def test_p1():
    assert(work_p1(test_input) == 3)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input, True) == 10440)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
