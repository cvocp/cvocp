# cvocp

Tools for phoneme clustering with the OCP. From the paper:
```
@InProceedings{hulden:2017:CoNLL,
  author    = {Hulden, Mans},
  title     = {A phoneme clustering algorithm based on the obligatory contour principle},
  booktitle = {Proceedings of The 21st SIGNLL Conference on Computational Natural Language Learning (CoNLL)},
  month     = {August},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics}
}
```

## ocpcluster.py

This is a stand-alone tool to perform phoneme/grapheme clustering on raw text.
Usage: `python ocpcluster.py textfile.txt`

Dependencies: [pydot](https://pypi.python.org/pypi/pydot/1.2.2)

Here, textfile.txt is assumed to be raw text, possibly with interword spacing.

Example: `python ocpcluster.py experiment1_data/spanish.txt` should produce the following hierarchical clustering:

![alt text](https://github.com/cvocp/cvocp/blob/master/spanish.cluster.png "Spanish clustering example")

## ocpclustertier.py

This is the tier-based variant of the above. It does the initial split identically to the previous (residue-based) algorithm, but then separates the corpus into *tiers* which are processed separately.

Usage: `python ocpclustertier.py textfile.txt`

Dependencies: [pydot](https://pypi.python.org/pypi/pydot/1.2.2)

The tier-based variant has a strong tendency to split (after the top-level C/V split) consonants into coronals and non-coronals, as well as split the vowel group into front/back (for small vowel systems), as seen in the example below. 

Example: `python ocpclustertier.py experiment1_data/spanish.txt`

![alt text](https://github.com/cvocp/cvocp/blob/master/spanish.cluster.2.png "Spanish clustering example")

## cvOCP.py

Python module to only do top-level clustering, i.e. learn a consonant-vowel distinction.

## sukhotin.py

Python module that implements Sukhotin's algorithm, based on the description by Jacques Guy in: Guy, J. (1991). Vowel Identification: an old (but good) algorithm. Cryptologia, 15(3):258-262.

## run503.py

Runs experiment 2 (infer C/V distinctions) on 503 Bible translations for all languages jointly in experiment2_data.

Usage: `python run503.py ocp` (for OCP algorithm) or `python run503.py sukhotin` (for Sukhotin's algorithm)

## run503i.py

Runs experiment 2 (infer C/V distinctions) on 503 Bible translations for all languages individually, reporting individual accuracies and macro-average in experiment2_data.

Usage: `python run503i.py ocp` (for OCP algorithm) or `python run503i.py sukhotin` (for Sukhotin's algorithm)

## mm.py

A reimplementation of the SVD-based method for unsupervised C/V classification in "Singular Value Analysis of Cryptograms", by Cleve Moler and Donald Morrison. The American Mathematical Monthly, Vol. 90, No. 2 (Feb., 1983), pp. 78-87.

### experiment1_data

Data files for an experiment in clustering phonemes in 9 languages. Note: while most of the symbols are IPA, some substitutions have been made to conform to `pydot` limitations.

### experiment2_data

Bible translations for 503 languages, from Kim & Snyder (2013).

### experiment3_data

Word lists (non-phonemic) for 10 languages, from the SIGMORPHON shared task.

### experiment4_data

The 54-symbol birch bark letter 292 in Cyrillic transcription.

### experiment4_data

Tier-based OCP experiment with graphemic data in 14 languages taken from Universal Dependencies 2.0.
