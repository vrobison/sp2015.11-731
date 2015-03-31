from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
from nltk import TrigramTagger as tt
from nltk.tag.hmm import HiddenMarkovModelTagger as HMMt

# Read the corpus into a list, 
# each entry in the list is one sentence.
cess_sents = cess.tagged_sents()

# Train the unigram tagger
uni_tag = ut(cess_sents)

sentence = "Hola , esta foo bar ."

# Tagger reads a list of tokens.
uni_tag.tag(sentence.split(" "))

# Split corpus into training and testing set.
train = int(len(cess_sents)*90/100) # 90%

# Train a bigram tagger with only training data.
bi_tag = bt(cess_sents[:train], backoff=uni_tag)

tri_tag = tt(cess_sents[:train], backoff=bi_tag)

#hmm_tag = HMMt.train(cess_sents[:train])

print 'UnigramTagger: %.1f %%' % (uni_tag.evaluate(cess_sents[train+1:]) * 100)
print 'BigramTagger: %.1f %%' % (bi_tag.evaluate(cess_sents[train+1:]) * 100)
print 'TrigramTagger: %.1f %%' % (tri_tag.evaluate(cess_sents[train+1:]) * 100)
#print 'HMM: %.1f %%' % (hmm_tag.evaluate(cess_sents[train+1:]) * 100)

# Evaluates on testing data remaining 10%
#bi_tag.evaluate(cess_sents[train+1:])

# Using the tagger.
#bi_tag.tag(sentence.split(" "))

import pickle

# Dump trained tagger
with open('unigram_spanish.pickle', 'w') as fd:
    pickle.dump(uni_tag, fd)
with open('bigram_spanish.pickle', 'w') as fd:
    pickle.dump(bi_tag, fd)
with open('trigram_spanish.pickle', 'w') as fd:
    pickle.dump(tri_tag, fd)
#with open('HMM_spanish.pickle', 'w') as fd:
#    pickle.dump(hmm_tag, fd)
# Load tagger
#with open('unigram_spanish.pickle', 'r') as fd:
 #   tagger = pickle.load(fd)
