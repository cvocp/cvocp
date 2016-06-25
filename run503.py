#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import sys
import codecs
import cvOCP
import sukhotin

datapath = 'experiment2_data/data'
onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]

vowellines = [line.strip() for line in codecs.open("experiment2_data/vowels.list", "r", encoding="utf-8")]
nonnasalconsonants = [line.strip() for line in codecs.open("experiment2_data/non_nasal_cons.list", "r", encoding="utf-8")]
nasallines = [line.strip() for line in codecs.open("experiment2_data/nasals.list", "r", encoding="utf-8")]

vowels_gold = set(vowellines)
consonants_gold = set(nonnasalconsonants + nasallines)
# Don't count y since it's ambiguous (as in Kim & Snyder, 2013)
consonants_gold.remove(u'y') 

print ("C (gold): [ " + ' '.join(consonants_gold) + ' ]').encode("utf-8")
print ("V (gold): [ " + ' '.join(vowels_gold) + ' ]').encode("utf-8")

lines = []
for lang in onlyfiles:
    lines += [line.strip() for line in codecs.open("experiment2_data/data/" + lang, "r", encoding="utf-8")]
    
data = []
tokencount = {}
for l in lines:
    word, count = l.split(u'@')
    lw = list(word)
    for char in lw:
        tokencount[char] = tokencount.get(char, 0) + int(count)

    data.append((lw, 1))


if sys.argv[1].startswith('s'):
    C, V = sukhotin.candv(data)
else:
    V, C = cvOCP.candv(data, random_seed = 64, verbose = True)
    # Without this seed, may need to run several times
    # to find global optimum (=5811245)
    # (there's a nasty local optimum at score: 5811243)

print "C:", ' '.join(C).encode("utf-8")
print "V:", ' '.join(V).encode("utf-8")

numcorrect = 0
numguesses = 0
numcorrecttoken = 0
numguessestoken = 0

for v in V:
    if v not in consonants_gold:
        numcorrect += 1
        numcorrecttoken += tokencount[v]
    else:
        print v, "WRONG (should be C)"
    numguessestoken += tokencount[v]
    numguesses += 1

for c in C:
    if c not in vowels_gold:
        numcorrect += 1
        numcorrecttoken += tokencount[v]
    else:
        print c, "WRONG (should be V)"
    numguesses += 1
    numguessestoken += tokencount[v]

print "[type]:"  + str(numcorrect/float(numguesses))[0:7]
print "[token]:" + str(numcorrecttoken/float(numguessestoken))[0:7]
