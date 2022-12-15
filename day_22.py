#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import math
import networkx as nx

test_input="""Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

class Node(object):
    def __init__(self, x, y, size, used, avail, percuse):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.percuse = percuse
    def __repr__(self):
        return repr(((self.x, self.y), self.size, self.used, self.avail))

def parse_input(inputs):
    re_int = re.compile("([0-9]+)")
    nodes = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers = re_int.findall(line)
        if numbers != None and len(numbers) == 6:
            numbers = [int(n) for n in numbers]
            nodes.append(Node(*numbers))
    return nodes

def work_p1(inputs):
    nodes = parse_input(inputs)
    
    ret = 0
    for i in range(len(nodes)):
        n1 = nodes[i]
        for j in range(i+1, len(nodes)):
            n2 = nodes[j]
            if n1.used != 0 and n1.used <= n2.avail or n2.used != 0 and n2.used <= n1.avail:
                ret += 1
    return ret

def work_p2(inputs):
    nodes = parse_input(inputs)
    
    paired_nodes = set()
    for i in range(len(nodes)):
        n1 = nodes[i]
        for j in range(0, len(nodes)):
            n2 = nodes[j]
            if n1.used != 0 and n1.used <= n2.avail or n2.used != 0 and n2.used <= n1.avail:
                paired_nodes.add(n1)
                paired_nodes.add(n2)
    
    empty_nodes = set(n for n in paired_nodes if n.used == 0)
    for n in empty_nodes:
        assert n in paired_nodes # sanity
    outliers = set(nodes) - paired_nodes
    
    # check that every not which is not an heavy weight can actually store the data of any other node
    # it means we can move data freely
    assert(min(m.size for m in paired_nodes) >= max(m.used for m in paired_nodes))
    # check that we have only one empty node
    assert(len(empty_nodes) == 1)
    empty_node = empty_nodes.pop()
    
    width = int(math.sqrt(len(nodes)))
    
    nodes = {(n.x, n.y): n for n in nodes}
    
    # print("")
    # for y in range(width):
    #     line = ""
    #     for x in range(width):
    #         n = nodes[(x,y)]
    #         if x == 0 and y == 0:
    #             line += "x"
    #         elif y == 0 and x == width - 1:
    #             line += "G"
    #         elif n in outliers:
    #             line += "#"
    #         elif n.used == 0:
    #             line += "_"
    #         else:
    #             line += "."
    #     print(line)
    # print("")
    
    # build an unoriented graph with all viable neighbour pairs
    G = nx.Graph()
    for y in range(width):
        for x in range(width):
            n1 = nodes[(x,y)]
            if n1 in outliers:
                continue
            if x != width - 1:
                n2 = nodes[(x+1, y)]
                if not n2 in outliers:
                    G.add_edge((x,y), (x+1, y))
            if y != width - 1:
                n3 = nodes[(x,y+1)]
                if not n3 in outliers:
                    G.add_edge((x,y), (x,y+1))
    
    # find the shortest number of moves to get an empty node to the left of the target node
    d = nx.shortest_path_length(G, (empty_node.x, empty_node.y), (width-2, 0))
    # print(nx.shortest_path(G, (empty_node.x, empty_node.y), (width-2, 0)))
    
    # little dance to get G to (0,0)...
    return d + 5*(width-2) + 1

def test_p1():
    assert(work_p1(test_input) == 7)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 7)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
