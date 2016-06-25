#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import codecs, math, sys
import cvOCP
import sukhotin

datapath = 'experiment2_data/data'
onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]

vowellines = [line.strip() for line in codecs.open("experiment2_data/vowels.list", "r", encoding="utf-8")]
nonnasalconsonants = [line.strip() for line in codecs.open("experiment2_data/non_nasal_cons.list", "r", encoding="utf-8")]
nasallines = [line.strip() for line in codecs.open("experiment2_data/nasals.list", "r", encoding="utf-8")]

vowels_gold = set(vowellines)
consonants_gold = set(nonnasalconsonants + nasallines)

print ("C:[ " + ' '.join(consonants_gold) + ' ]').encode("utf-8")
print ("V:[ " + ' '.join(vowels_gold) + ' ]').encode("utf-8")

if sys.argv[1].startswith('s'):
    sukh_alg = True
else:
    sukh_alg = False

numiter = 0
guesstype = 0.0
guesstoken = 0.0
for lang in onlyfiles:
    lines = [line.strip() for line in codecs.open("experiment2_data/data/" + lang, "r", encoding="utf-8")]
    
    data = []
    originaldata = []
    appearances = {}
    originalappearances = {}

    for l in lines:
        word, count = l.split(u'@')
        lw = list(word)
        for x in set(lw):
            appearances[x] = appearances.get(x, 0) + 1
            # To compare with Kim & Snyder, only do token counts
            # on items seen >= 5 times
            # "For our experiments, we extracted unique word types 
            # occurring at least 5 times" (K&S 2012, p.6)
            if count >= 5:
                originalappearances[x] = originalappearances.get(x, 0) + int(count)

    for l in lines:
        word, count = l.split(u'@')
        lw = list(word)
        if count > 1 and all(appearances[x] > 3 for x in set(lw)):
            originaldata.append((lw, int(count)))
            data.append((lw, 1))

    if sukh_alg == True:
        C, V = sukhotin.candv(data)
    else:
        C, V = cvOCP.candv(data)
        num1 = sum(v in vowels_gold for v in V)
        num2 = sum(v in consonants_gold for v in V)
        if num1 < num2:  # OCP only gives us two sets.
            C, V = V, C  # 99% of the time, the smaller set is V
                         # but we give the algorithm the benefit of the doubt
                         # by picking the better division.

    print "C:", ' '.join(C).encode("utf-8")
    print "V:", ' '.join(V).encode("utf-8")
    C = C - {'y'}
    V = V - {'y'}
    numcorrecttype = 0
    numguessestype = 0
    numcorrecttoken = 0
    numguessestoken = 0
    print "WRONG:",
    for v in V:
        if v in originalappearances:
            if v not in consonants_gold:
                numcorrecttype += 1
                numcorrecttoken += originalappearances[v]
            else:
                print v,
            numguessestype += 1
            numguessestoken += originalappearances[v]

    for c in C:
        if c in originalappearances:
            if c not in vowels_gold:
                numcorrecttype += 1
                numcorrecttoken += originalappearances[c]
            else:
                print c,
            numguessestype += 1
            numguessestoken += originalappearances[c]
    print
    print lang + '[type]:' + str(numcorrecttype/float(numguessestype))[0:6]
    print lang + '[token]:' + str(numcorrecttoken/float(numguessestoken))[0:6]
    numiter += 1
    guesstype += numcorrecttype/float(numguessestype)
    guesstoken += numcorrecttoken/float(numguessestoken)

print "type average:", guesstype/float(numiter)
print "token average:", guesstoken/float(numiter)
