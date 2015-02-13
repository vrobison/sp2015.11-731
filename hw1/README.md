There are three Python programs here (`-h` for usage):

 - `./align` aligns words using Dice's coefficient.
 - `./check` checks for out-of-bounds alignment points.
 - `./grade` computes alignment error rate.

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./align -t 0.9 -n 1000 | ./check | ./grade -n 5


The `data/` directory contains a fragment of the German/English Europarl corpus.

 - `data/dev-test-train.de-en` is the German/English parallel data to be aligned. The first 150 sentences are for development; the next 150 is a blind set you will be evaluated on; and the remainder of the file is unannotated parallel data.

 - `data/dev.align` contains 150 manual alignments corresponding to the first 150 sentences of the parallel corpus. When you run `./check` these are used to compute the alignment error rate. You may use these in any way you choose. The notation `i-j` means the word at position *i* (0-indexed) in the German sentence is aligned to the word at position *j* in the English sentence; the notation `i?j` means they are "probably" aligned.


IBM_Model1 is my implementation of the IBM Model 1.

IBMsplit is the IBM Model 1 augmented to have compound splitting. If a German word can be split into two substrings that are both observed words, it splits it and adds the split pieces before continuing with the IBM model, and after the alignment is complete, the indexes are returned to those of the original words. I tried replaceing the original word with the splits, but found it was worse than the base line and having both performed very slightly better. It also has some crude stemming,  mostly to catch regular plurals in both languages but that will also catch lots of German verbs--to be improved.

symmeterized has symmeterization, grow-diag, and final-and. I got rid of the inneficient compound splitting above and ran it on a lowercased version of the bitext.

compoundsplit has everything in symmeterized but also handles inputting a copy of the German text after being run through the cdec compound splitter, using the split text to train, and aligns using the original indices.--aborted due to pipe issues, too late to fix now before midnight
