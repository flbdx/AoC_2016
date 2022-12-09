#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

def work_p1(lines, width_=50, height_=6):
    width = width_
    height = height_
    grid = {}
    for x in range(width):
        for y in range(height):
            grid[x,y] = 0

    re_line = re.compile(r"(rect |rotate row y=|rotate column x=)(\d+)(x| by )(\d+)")
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        m = re_line.match(line)
        m1, m2 = int(m.group(2)), int(m.group(4))
        if line.startswith("rect"):
            w, h = m1, m2
            for x in range(w):
                for y in range(h):
                    grid[x,y] = 1
        elif line.startswith("rotate row"):
            y, n = m1, m2
            l = [grid[x,y] for x in range(width)]
            for x in range(width):
                grid[x,y] = l[(x - n) % width]
        else:
            x, n = m1, m2
            l = [grid[x,y] for y in range(height)]
            for y in range(height):
                grid[x,y] = l[(y - n) % height]
                
    for y in range(height):
        print("".join('#' if grid[x,y] == 1 else ' ' for x in range(width)))
    print("")
        
    return sum(grid.values())

def p1_p2():
    print(work_p1(fileinput.input()))
p1_p2()
