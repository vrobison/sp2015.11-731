There are three Python programs here (`-h` for usage):

 - `./evaluate` evaluates pairs of MT output hypotheses relative to a reference translation using counts of matched words
 - `./check` checks that the output file is correctly formatted
 - `./grade` computes the accuracy

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./evaluate | ./check | ./grade


The `data/` directory contains the following two files:

 - `data/train-test.hyp1-hyp2-ref` is a file containing tuples of two translation hypotheses and a human (gold standard) translation. The first 26208 tuples are training data. The remaining 24131 tuples are test data.

 - `data/train.gold` contains gold standard human judgements indicating whether the first hypothesis (hyp1) or the second hypothesis (hyp2) is better or equally good/bad for training data.

Until the deadline the scores shown on the leaderboard will be accuracy on the training set. After the deadline, scores on the blind test set will be revealed and used for final grading of the assignment.

normstemSnowball: stems using Snowball stemmer, removes accent marks nlyk tool can't handle 

stemplusMETEOR: takes output of normstemSnowball, scores on tri- bi- and unigrams, full points for exact matches, partial points for stem matches, tuned parameters controlling partial point value and precision/recall tradeoff.

stem_func_len: tri- bi- and unigrams, full points for exact matches, partial points for function word unigrams (list of function words copied from ladognome), partial ponts for stem matches, and tuned recall-precision tradeoff.

WordNet synonym matching attemped, but runs slow as molasses and was thus abandoned, functions included but calls to them are commented out.
