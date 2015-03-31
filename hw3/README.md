swap_optional is based of eschlinger(Eva)'s initial commit, but decodes both the original sentence and one that has had noun-adj sequences flipped to a more English-like order, then picks the more probable translation. The sentence is POS tagged using a tagger trained on the CESS Spanish corpus, and identified nouns followed by adjectives are swapped. Allowing untagged words followed by adjectives to swap like adjective-noun pairs has a slightt benefit.

train_ES_POS_tagger trains unigram, bigram, and trigram taggers on the CESS  Spanish corpus. The HMM tagger was also trained and evaluated, but performed worse than the ngram taggers on the held out test set and pickle wasn't saving it properly, so it wasn't tested on the assignment data. The different n-gram taggers don't perform measurably differently since the unswapped sentences are picked more often--the impact of the swapped options is minimal. Only using swapped sentences is worse thean the original.



There are three Python programs here (`-h` for usage):

 - `./decode` a simple non-reordering (monotone) phrase-based decoder
 - `./grade` computes the model score of your output

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./decode | ./grade


The `data/` directory contains the input set to be decoded and the models

 - `data/input` is the input text

 - `data/lm` is the ARPA-format 3-gram language model

 - `data/tm` is the phrase translation model

