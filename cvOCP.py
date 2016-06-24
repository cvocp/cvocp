############################################################################
# The OCP-based algorithm for only determining the top-level cluster, i.e. #
# only determining consonants and vowels (or syllabic, non-syllabic).      #
#                                                                          #
# Usage:                                                                   #
#                                                                          #
# import cvOCP                                                             #
# C,V = cvOCP.candv(data)                                                  #
#                                                                          #
# where data is an iterable of 2-tuples (tokenized_word, occurrence_count) #
#                                                                          #
# Example:                                                                 #
# >>> import cvOCP                                                         #
# >>> data = [ (('a','b','e','g','a'),2), (('e','k','a','g'), 3) ]         #
# >>> cvOCP.candv(data)                                                    #
# (set(['k', 'b', 'g']), set(['a', 'e']))                                  #
#                                                                          #
# This returns two sets of strings, C and V.                               #
############################################################################

import random, itertools

class listset:
    def __init__(self, text):
        """Text is list of tokenized words, with counts."""
        # [ (('a','b','e','gh'),1), (('a','k','a'), 3) ]
        self.allsegments = set()
        for pair, count in text:
            for segment in pair:
                self.allsegments.add(segment)

        self.bigramcounts = {}
        for pair, count in text:
            for idx in xrange(len(pair)-1):
                self.bigramcounts[pair[idx] + pair[idx+1]] = self.bigramcounts.get(pair[idx] + pair[idx+1], 0) + count

        self.tree = {}
        self.tree[''] = self.allsegments
        self.tree['0'], self.tree['1'] = self._randsplitset(self.allsegments)

    def split(self, set1):
        self.tree[set1 + '0'] = self.tree[set1]
        self.tree[set1 + '1'] = set()
               
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

    def _score(self, set1, set2):
        sc = 0
        for bi in self.bigramcounts:
            if (bi[0] in set1 and bi[1] in set2) or (bi[0] in set2 and bi[1] in set1):
                sc += self.bigramcounts[bi]
        return sc

    def _randsplitset(self, s):
        """Splits a set randomly into two subsets."""
        setlist = list(s)
        random.shuffle(setlist)
        R = random.randint(0,len(setlist))
        return set(setlist[0:R]), set(setlist[R:])
   
def candv(data, random_seed = None, verbose = False):
    if random_seed:
        random.seed(random_seed)

    # [ (('a','b','c','gh'),1), (('a','k','a'), 3) ]
    """Data is assumed to be this format."""

    ls = listset(data)

    def genperms(x):    
        barelist = ["".join(seq) for n in xrange(1,x) for seq in itertools.product("01", repeat=n)]    
        return [(barelist[i], barelist[i+1]) for i in xrange(0, len(barelist),2)]

    for sets in genperms(2):
        if sets[0] in ls.tree and sets[1] in ls.tree:
            zero = ls.tree[sets[0]]
            one = ls.tree[sets[1]]
            bestzero = zero
            bestone = one
            for iter in xrange(1200): # run 1200 top-level iterations
                bestscore = ls._score(zero, one)
                for i in xrange(150): #for every change in cooling, run 150 times  
                    rs = int(1+(1/float(iter + 1))*2000) # Annealing schedule determines how many swaps to make drawn from uniform distribution
                    newzero, newone = ls._randomswap(rs, zero, one)
                    newscore = ls._score(newzero, newone)
                    if newscore > bestscore:
                        bestzero = newzero
                        bestone = newone
                        if verbose:
                            print 'Oldscore:', bestscore, 'Newscore:', newscore, '\n{', ' '.join(newzero).encode("utf-8"), '}\n' , '{' , ' '.join(newone).encode("utf-8"), '}'
                        bestscore = newscore
                zero = bestzero
                one = bestone

            if ls.tree[sets[0]] != zero and ls.tree[sets[0]] != one:
                ls.tree[sets[0]] = zero
                ls.tree[sets[1]] = one
                if len(zero) > 1:
                    ls.split(sets[0])
                if len(one) > 1:
                    ls.split(sets[1])

    for par in genperms(8):    
        for p in par:
            if p in ls.tree and p + '0' in ls.tree and p + '1' in ls.tree:
                if ls.tree[p + '0'] == ls.tree[p] or ls.tree[p + '1'] == ls.tree[p]:
                    del ls.tree[p + '0']
                    del ls.tree[p + '1']

    C = ls.tree['0']
    V = ls.tree['1']

    if verbose:
        print "SCORE:", bestscore
    if len(C) < len(V):
        C, V = V, C
    return C, V
