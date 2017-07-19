"""
A Python reproduction of the SVD method in the article
"Singular Value Analysis of Cryptograms"
by Cleve Moler and Donald Morrison
The American Mathematical Monthly, Vol. 90, No. 2 (Feb., 1983), pp. 78-87

The original paper classifies segments into three classes:
C, V, and N (unknown) using the signs of the left and right components of the
rank 2 approximation.  The classification here forces all segments into either
C or V (i.e. never N) by checking the difference of  x_i2 - y_i2
This gives the same result for all segments that would be classified as C or V
by the original algorithm, and forces an N into whichever is "closer", C or V.

Author: Mans Hulden
Last Update: 8/2/2016
"""

import numpy as np

def candv(data):
    # data = [ (('a','b','c','a'),1), (('a','k','a'), 3) ]
    """Data is assumed to be in this format, i.e. an iterable
       of pairs of tokenized words and occurrence counts.
       We return two sets, C and V.  Example:
       >>> data = [ (('a','b','a'),1), (('a','c','a'), 3) ]
       >>> mm.candv(data)
       (set(['c', 'b']), set(['a']))
       """

    alphabet = {l for w, _ in data for l in w}
    atoi = {x:y for x,y in zip(alphabet, range(len(alphabet)))}
    itoa = {v:k for k,v in atoi.iteritems()}
    G = np.zeros((len(alphabet),len(alphabet)))

    for word, count in data:
        for l,r in zip(word, word[1:]):
            G[atoi[l]][atoi[r]] += count

    X, _ , Y = np.linalg.svd(G, full_matrices=True)

    C, V = set(), set()

    for lnum in range(X.shape[0]):
        if X[:,1][lnum] - Y[1][lnum] >= 0:
            V.add(itoa[lnum])
        else:
            C.add(itoa[lnum])

    return C, V
    
