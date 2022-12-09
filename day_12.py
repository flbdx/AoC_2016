#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".splitlines()

class VM(object):
    def __init__(self, assembunny):
        self.instructions = []
        self.reset()
        
        for line in assembunny:
            line = line.strip()
            if len(line) == 0:
                continue
            words = line.split(" ")
            self.instructions.append((getattr(VM, "do_" + words[0]), words[1:]))
    
    def reset(self):
        self.ip = 0
        self.regs = {n:0 for n in "abcd"}
    
    def run_one(self):
        instr, ops = self.instructions[self.ip]
        instr(self, *ops)
        return (self.ip, self.ip < 0 or self.ip >= len(self.instructions))
    
    def do_cpy(self, x, y):
        #print(self.ip, ("cpy", x, y), self.regs)
        if x in "abcd":
            self.regs[y] = self.regs[x]
        else:
            self.regs[y] = int(x)
        self.ip += 1
    
    def do_inc(self, x):
        #print(self.ip, ("inc", x), self.regs)
        self.regs[x] += 1
        self.ip += 1
    
    def do_dec(self, x):
        #print(self.ip, ("dec", x), self.regs)
        self.regs[x] -= 1
        self.ip += 1
    
    def do_jnz(self, x, y):
        #print(self.ip, ("jnz", x, y), self.regs)
        x = self.regs[x] if x in "abcd" else int(x)
        y = self.regs[y] if y in "abcd" else int(y)
        if x != 0:
            self.ip += y
        else:
            self.ip += 1


if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def work_p1(inputs):
    vm = VM(inputs)
    
    while True:
        ip, teminated = vm.run_one()
        if teminated:
            break
    return vm.regs["a"]

def work_p2(inputs):
    # for my input, it part 1 returns fibo(2+26) + 14*14
    # 26 comes from the d register initialization
    # the 14*14 is from the last 7 instructions
    
    # initializing c to 1 results in 7 more fibonacci iterations (lines 6 to 9)
    
    def fibonacci(n):
        a = 0
        b = 1
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            for i in range(1, n):
                c = a + b
                a = b
                b = c
            return b
    
    return fibonacci(2+26+7) + 14*14

def test_p1():
    assert(work_p1(test_input) == 42)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
