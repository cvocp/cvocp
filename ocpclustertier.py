#!/usr/bin/env python
"""
Usage: python ocpcluster.py textfile.txt [threshold]

Splits segments by OCP-based algorithm and draws hierarchical graph
Dependencies: pydot (for cluster drawing)

The input file is assumed to be unpunctuated text, possibly with
newlines (they are ignored).

The threshold is used to filter out words that contain character
with fewer than [threshold] occurrences in the whole corpus (default 1).

Author: Mans Hulden
Last Update: 5/30/2017
"""


import re
import random
import itertools
import codecs
import pydot
import os
import sys

class listset:
    def __init__(self, text):
        self.texts = {}
        self.texts['0'] = text
        self.texts['1'] = text
        self.allsegments = {x for x in text if x != ' '}
        self.bgcounts = {}
        self.bgcounts['0'] = {}
        bigrams = [x[0] + x[1] for x in zip(text, text[1:])]
        for bi in bigrams:
            if bi[0] != ' ' and bi[1] != ' ':
                self.bgcounts['0'][bi] = self.bgcounts['0'].get(bi, 0) + 1
        self.bgcounts['1'] = self.bgcounts['0']

        self.tree = {}
        self.tree[''] = self.allsegments
        self.texts[''] = text  # every node in the tree has a text
        self.tree['0'], self.tree['1'] = self._randsplitset(self.allsegments)

    def split(self, set1):
        """Do a new split from XXX -> XXX0 and XXX1."""
        self.tree[set1 + '0'] = self.tree[set1]
        self.tree[set1 + '1'] = set()
        newtext = ''.join(c for c in self.texts[set1] if c in self.tree[set1] or c in ' ')
        newtext = ' '.join(newtext.split())
        newbigrams = [x[0] + x[1] for x in zip(newtext, newtext[1:])]
        self.bgcounts[set1 + '0'] = {}
        self.bgcounts[set1 + '1'] = {}    
        for bi in newbigrams:
            if bi[0] != ' ' and bi[1] != ' ':
                self.bgcounts[set1 + '0'][bi] = self.bgcounts[set1 + '0'].get(bi, 0) + 1
        self.bgcounts[set1 + '1'] = self.bgcounts[set1 + '0']
        self.texts[set1 + '1'] = newtext
        self.texts[set1 + '0'] = newtext
               
    def _randomswap(self, n, set1, set2):
        if len(set1) == 0:
            one = set([])
        else:
            maxn = min(n, len(set1)-1)
            numswap1 = random.randint(0, maxn)
            one = set(random.sample(set1, numswap1))
        if len(set2) == 0:
            two = set([])
        else:
            maxn = min(n, len(set2)-1)
            numswap2 = random.randint(0, maxn)
            two = set(random.sample(set2, numswap2))
        return (set1 - one) | two, (set2 - two) | one

    def _score(self, set1, set2, treepos):
        sc = 0
        for bi in self.bgcounts[treepos]:
            if (bi[0] in set1 and bi[1] in set2) or (bi[0] in set2 and bi[1] in set1):
                sc += self.bgcounts[treepos][bi]
        return sc

    def _randsplitset(self, s):
        """Splits a set randomly into two subsets."""
        setlist = list(s)
        random.shuffle(setlist)
        R = random.randint(0,len(setlist))
        return set(setlist[0:R]), set(setlist[R:])
   
with codecs.open(sys.argv[1], "r", "utf-8") as myfile:
    data = " ".join(line.rstrip() for line in myfile)


if len(sys.argv) > 2:
    minoccurrences = int(sys.argv[2])

    charfreq = {}
    for s in data:
        charfreq[s] = charfreq.get(s, 0) + 1

    words = data.split(' ')
    fwords = [x for x in words if all(charfreq[y] > minoccurrences for y in x)]
    data = ' '.join(fwords)

ls = listset(data)

def genperms(x):    
    barelist = ["".join(seq) for n in xrange(1,x) for seq in itertools.product("01", repeat=n)]    
    return [(barelist[i], barelist[i+1]) for i in xrange(0, len(barelist),2)]

for sets in genperms(9):
    if sets[0] in ls.tree and sets[1] in ls.tree:
        zero = ls.tree[sets[0]]
        one = ls.tree[sets[1]]
        bestzero = zero
        bestone = one
        for iter in xrange(1200):
            bestscore = ls._score(zero, one, sets[0])
            for i in xrange(150):
                rs = int(1+(1/float(iter + 1))*2000) # Annealing schedule determines how many swaps to make
                newzero, newone = ls._randomswap(rs, zero, one)
                newscore = ls._score(newzero, newone, sets[0])
                if newscore > bestscore:
                    bestzero = newzero
                    bestone = newone
                    print bestscore, newscore, '{', ' '.join(newzero).encode("utf-8"), '}', '{' , ' '.join(newone).encode("utf-8"), '}', iter, rs
                    #print bestscore, newscore, newzero, newone, iter, rs
                    bestscore = newscore
            zero = bestzero
            one = bestone
        if ls.tree[sets[0]] != zero and ls.tree[sets[0]] != one:
            ls.tree[sets[0]] = zero
            ls.tree[sets[1]] = one
            if len(zero) > 1:
                ls.split(sets[0])
                print "SPLITTING:", sets[0]
            if len(one) > 1:
                ls.split(sets[1])
                print "SPLITTING:", sets[1]

for par in genperms(8):    
    for p in par:
        if p in ls.tree and p + '0' in ls.tree and p + '1' in ls.tree:
            if ls.tree[p + '0'] == ls.tree[p] or ls.tree[p + '1'] == ls.tree[p]:
                del ls.tree[p + '0']
                del ls.tree[p + '1']


for k in sorted(ls.tree.keys()):
    print k + ":",
    for w in sorted(list(ls.tree[k])):
        print w,
    print
    
graph = pydot.Dot(graph_type='graph')

for k in ls.tree:
    s0 = u"\u00a0".join(sorted(list(ls.tree[k])))
    s0 = s0.encode('utf-8')    
    if k + '0' in ls.tree:
        s00 = u"\u00a0".join(sorted(list(ls.tree[k + '0'])))
        s00 = s00.encode('utf-8')
        edge = pydot.Edge(s0,s00)
        graph.add_edge(edge)
    if k + '1' in ls.tree:
        s01 = u"\u00a0".join(sorted(list(ls.tree[k + '1'])))
        s01 = s01.encode('utf-8')
        edge = pydot.Edge(s0,s01)
        graph.add_edge(edge)

graph.write_pdf("example1_graph.pdf")
os.system("open example1_graph.pdf")
