#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

sample_input="""value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

def work(lines, comps=(17,61), part=1):
    re_init = re.compile(r"value (\d+) goes to bot (\d+)")
    re_gives = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
    
    bots = {}
    outputs = {}
    rules = {}
    
    next_bot = []
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        m = re_init.match(line)
        if m:
            v = int(m.group(1))
            b = int(m.group(2))
            bots[b] = bots.get(b, []) + [v]
            if len(bots[b]) == 2:
                next_bot.append(b)
        
        else:
            m = re_gives.match(line)
            bs = int(m.group(1))
            tl = m.group(2)
            nl = int(m.group(3))
            th = m.group(4)
            nh = int(m.group(5))
            
            rules[bs] = (tl, nl, th, nh)
    
    while len(next_bot) != 0:
        bot = next_bot.pop(0)
        vl = min(bots[bot])
        vh = max(bots[bot])
        
        if part==1 and vl == comps[0] and vh == comps[1]:
            return bot
        
        tl, nl, th, nh = rules[bot]
        
        if tl == "bot":
            bots[nl] = bots.get(nl, []) + [vl]
            if len(bots[nl]) == 2:
                next_bot.append(nl)
        else:
            outputs[nl] = outputs.get(nl, []) + [vl]
        
        if th == "bot":
            bots[nh] = bots.get(nh, []) + [vh]
            if len(bots[nh]) == 2:
                next_bot.append(nh)
        else:
            outputs[nh] = outputs.get(nh, []) + [vh]
    
    return outputs[0][0] * outputs[1][0] * outputs[2][0]
        
def test_p1():
    assert(work(sample_input.splitlines(), (2,5)) == 2)
test_p1()

def p1():
    print(work(fileinput.input()))
p1()

def p2():
    print(work(fileinput.input(), part=2))
p2()
