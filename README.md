# cvocp

Tools for phoneme clustering with the OCP.

## ocpcluster.py

This is a stand-alone tool to perform phoneme/grapheme clustering on raw text.
Usage: `python ocpcluster.py textfile.txt`

Dependencies: _pydot_

Here, textfile.txt is assumed to be raw text, possibly with interword spacing.

Example: `python ocpcluster.py experiment1_data/spanish.txt` should produce the following hierarchical clustering:

![alt text](https://github.com/cvocp/cvocp/blob/master/spanish.cluster.png "Spanish clustering example")

## cvOCP.py

Python module to only do top-level clustering, i.e. learn a consonant-vowel distinction.

## sukhotin.py

Python module that implements Sukhotin's algorithm.

### experiment1_data

Data files for an experiment in clustering phonemes in 9 languages.

### experiment2_data

Bible translations for 503 languages, from Kim & Snyder (2013).

### experiment3_data

Word lists (non-phonemic) for 10 languages, from the SIGMORPHON shared task.

### experiment4_data

The 54-symbol birch bark letter 292 in Cyrillic transcription.
