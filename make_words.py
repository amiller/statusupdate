from nltk.corpus import brown
import nltk
import cPickle as pickle
import os

def get_all_words(corp=brown):
    parts = """
    VBG
    VBD
    JJ
    NN
    NNS
    NP
    VB
    """.strip().split()
    d = {}
    for pos in parts:
        d[pos] = get_words(corp, pos)
        print '%s [%d]' % (pos, len(d[pos]))
    with open('words.pkl','w') as f:
        pickle.dump(d, f)


def get_words(corp=brown, pos='NN'):
    N = [word for word,_pos in corp.tagged_words() if _pos==pos]
    return N


def load_words():
    global words
    with open('words.pkl','r') as f:
        words = pickle.load(f)

if not 'words' in globals():
    load_words()
