###########################################################################
# Sukhotin's Algorithm for determining consonants and vowels in a corpus  #
# Based on the description by Jacques Guy in:                             #
# Guy, J. (1991). Vowel Identification: an old (but good) algorithm.      #
# Cryptologia, 15(3):258-262.                                             #
# Author:                                                                 #
# - 20160517                                                              #
###########################################################################

def candv(data, diagonal = False):
    # data = [ (('a','b','c','gh'),1), (('a','k','a'), 3) ]
    """Data is assumed to be this format, i.e. an iterable 
       of pairs of tokenized words and occurrence counts.
       We return two sets, C and V.
       Example:
       C,V = sukhotin.candv(data).
       The diagonal argument controls whether co-occurrence 
       of a segment with itself should be taken into account.
       Sukhotin's description doesn't, but doing so sometimes
       gives better results."""

    C = {l for w, _ in data for l in w}
    m = {l:{} for l in C}
    for word, count in data:
        for l,r in zip(word, word[1:]):
            if l != r or diagonal:
                m[l][r] = m[l].get(r, 0) + count
                m[r][l] = m[r].get(l, 0) + count
    
    V = set()
    sums = {x:sum(m[x].values()) for x in m.keys()}
    while True:
        newvowel = max(sums, key = sums.get)
        if sums[newvowel] < 0:
            break
        V.add(newvowel)
        C.remove(newvowel)
        sums.pop(newvowel)
        for c in C:
            sums[c] = sums[c] - 2 * m[c].get(newvowel, 0)

    return C, V
