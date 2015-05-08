My baseline implementation is apparently freakishly fast compared to everyone I've talked to, making me suspect something is wonky, otherwise I just haven't found the right combination of alpha/gamma/iterations over the training set. Several attempts to predict case using lexical context or the POS of the context made results worse; I expected these to at least pick up prepositional and genetive case stuff. So any additional time I can spare on this will go into better case prediction.

rerank4: best baseline so far
case: case prediction attempt #1, lexical
case3: case prediction attempt #3, syntactic (attempt 2 similar, but more broken, not pushed to public)

-----------------update----------------
Something funny is going on. I've run Seven's rerank_dict with the parameters specified in her readme and got different results, so either I'm not understanding her readme corectly, it has an error, or my computer thinks 2+2=5. (I think I also ran kk's code earlier in the week and likewise got a lower MRR than he reports.) I've already double- and triple-checked that my data is correctly updated. I can now pass the baseline on the dev set reliably (though not by much) using only the training data, but still crash and burn on the test set.

all_copied_features2: souped up with a bunch more features gleaned from other student's code-I think this version copies features from Yohan and Perilon

There are three Python programs here (`-h` for usage):

 - `./rerank` a simple reranker that simply sorts candidate translations on log p(czech|english)
 - `./grade` computes the mean reciprocal rank of your output

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./rerank | ./check | ./grade


The `data/` directory contains the input set to be decoded and the models

 - `data/train.input` is the input side of training set in the format described on the homework webpage

 - `data/train.refs` are the references to the training set, giving the correct czech translation for the highlighted phrase in each sentence

 - `data/train.parses` are dependency parses of the training sentences, provided for convenience. (Note: these files are provided in gzip format to avoid the space limitations imposed by github)

 - `data/dev+test.input` is the input side of both the dev and test sets

 - `data/dev.refs` are the references to the dev set, which is the first half of the above dev+test file

 - `data/dev+test.parses` are dependency parses of the dev and test sentences, provided for convenience

 - `data/ttable` is the phrase translation table which contains candidates that you will rerank

 If you want the raw parallel data used to build the training data and translation tables English-Czech data (for example, to build word vectors), it is available at http://demo.clab.cs.cmu.edu/sp2015-11731/parallel.encs .
