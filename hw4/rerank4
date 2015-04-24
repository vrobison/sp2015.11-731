#!/usr/bin/env python
import sys
import argparse
import numpy as np
from scipy.sparse import csr_matrix
import random

from collections import defaultdict
from utils import read_ttable

def dot(f, w):
	s = 0.0
	for k in f.keys():
		s += f[k] * w[wvocabulary[k]]
	return s

def updatew(wi,xcy,ynot):
	a = 0.1
	dLdw = {}
	dLdw[xcy[1]] = -1.0
	dLdw[xcy[2]] = -1.0
	dLdw[ynot[1]] = 1.0
	dLdw[ynot[2]] = 1.0	
	for f in ynot[4].keys(): 
		dLdw[f] = ynot[4][f] - xcy[4][f] 
	adLdw = {}
	for i in dLdw.keys():
		adLdw[i] = a*dLdw[i]
	wiplus = wi
	for k in adLdw.keys():
		wiplus[wvocabulary[k]] = (wi[wvocabulary[k]] - adLdw[k])
	return wiplus

def L(xcy,ynot,g):
	#xcy: (x,prev,next,y*,feats)
	#ynot: (x,prev,next,y-,feats2)
 	#0.000005 0.387528 #1->0.390202 
	#indexes in w of form f1,f2,f3,f4,x_y_cleft, x_y_cright
	#for ynot in fxcynot: #for each wrong y
	diff = {}
	for f in ynot[4].keys(): #
		diff[f] = ynot[4][f] - xcy[4][f]
	#diff in float features
	diff[xcy[1]] = 1.0
	diff[xcy[2]] = 1.0
	diff[ynot[1]] = -1.0
	diff[ynot[2]] = -1.0
	m = max(0, (g-dot(diff, weights)))
	return m

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', default='data/dev+test.input')
parser.add_argument('--train','-tr',default='data/train.input')
parser.add_argument('--refs', '-r',default='data/train.refs')
parser.add_argument('--ttable', '-t', default='data/ttable')
args = parser.parse_args()

translation_table = read_ttable(args.ttable)
startweights = {'log_prob_tgs': 1.0,'log_prob_sgt': 1.0,'log_lex_prob_tgs':1.0,'log_lex_prob_sgt':1.0} #simple weight vector (1 0 0 0)

windptr = [0]
windices = []
wdata = []
wvocabulary = {}
ALLcsr = []

for f in startweights.keys():
	windex = wvocabulary.setdefault(f,len(wvocabulary))
	windices.append(windex)
	wdata.append(startweights[f])
	
ix = []
indptr = [0]
indices = []
data = []
vocabulary = {}
for l, line in enumerate(open(args.train)):
	left_context, phrase, right_context = [part.strip() for part in line.decode('utf-8').strip().split('|||')]
	candidates = [(target,features) for target, features in translation_table[phrase].iteritems()]	
	xcynot = []	
	
	for y,feat in candidates:
		left_context = ('<s> '+left_context).strip()
		right_context = (right_context + ' <\s>').strip()
		if len(left_context.split()) > 1:
			left_context = left_context.split()[-1]
		if len(right_context.split()) > 1:
			right_context = right_context.split()[0]
		prev = 'src:'+phrase+'_tgt:'+y+'_prev:'+left_context
		next = 'src:'+phrase+'_tgt:'+y+'_next:'+right_context

		windex = wvocabulary.setdefault(prev, len(wvocabulary))
		windices.append(windex)
		wdata.append(0.0)

		windex = wvocabulary.setdefault(next, len(wvocabulary))
		windices.append(windex)
		wdata.append(0.0)

windptr.append(len(windices))
#feats = csr_matrix((data,indices,indptr),dtype=float).toarray()
#print wvocabulary
				#print feats
weights = csr_matrix((wdata,windices,windptr),dtype=float).toarray()
weights = weights[0]

vocabset = set()
for v in wvocabulary.keys():
	vocabset.add(v)
sys.stderr.write('finished weight setup')
#print weights
#sys.stderr.write(str(len(feats[0]))+' '+str(len(weights[0]))+' '+str(len(ix)))

reffile = open(args.refs).readlines()
refs =[]
for r in reffile: refs.append(r.strip())

for iteration in range(5): #4
	data = []
	for l, line in enumerate(open(args.train)):
		data.append((line + ' ||| '+refs[l]))
	random.shuffle(data)
	for l, line in enumerate(data):
		left_context, phrase, right_context,ref = [part.strip() for part in line.decode('utf-8').strip().split('|||')]
		
		candidates = [(target,features) for target, features in sorted(translation_table[phrase].iteritems(), key=lambda (t, f): dot(f, weights), reverse=True)]	
		xcynot = []
		n = 0
		left_context = ('<s> '+left_context).strip()
		right_context = (right_context + ' <\s>').strip()
		if len(left_context.split()) > 1:
			left_context = left_context.split()[-1]
		if len(right_context.split()) > 1:
			right_context = right_context.split()[0]
		for (y,origfeat) in candidates:
			prev = 'src:'+phrase+'_tgt:'+y+'_prev:'+left_context
			next = 'src:'+phrase+'_tgt:'+y+'_next:'+right_context
			if y == ref:
				xcy = (phrase, prev, next, y, origfeat)
			else: 
				xcynot.append((phrase, prev, next, y, origfeat)) #incorrect
		for ynot in xcynot:
			if L(xcy,ynot,2) != 0:
				weights = updatew(weights,xcy,ynot)
sys.stderr.write('finished training')

for line in open(args.input):
	left_context, phrase, right_context = [part.strip() for part in line.decode('utf-8').strip().split('|||')]
	candidates = [(target,features) for target, features in sorted(translation_table[phrase].iteritems(), key=lambda (t, f): dot(f, weights), reverse=True)]
	c2 = []
	left_context = ('<s> '+left_context).strip()
	right_context = (right_context + ' <\s>').strip()
	if len(left_context.split()) > 1:
		left_context = left_context.split()[-1]
	if len(right_context.split()) > 1:
		right_context = right_context.split()[0]
	for (y,feat) in candidates:
		prev = 'src:'+phrase+'_tgt:'+y+'_prev:'+left_context
		next = 'src:'+phrase+'_tgt:'+y+'_next:'+right_context
		if prev in vocabset: feat[prev] = 1
		if next in vocabset: feat[next] = 1
		#if prev in wvocabulary.keys(): feat[prev] = 1
		#if next in wvocabulary.keys(): feat[next] = 1 
		c2.append((y,dot(feat,weights)))
	c3 = sorted(c2, key=lambda x: x[1], reverse=True)
	cfinal = []
	for i in range(len(c3)):
		cfinal.append(c3[i][0])
	print ' ||| '.join(cfinal).encode('utf-8')
	sys.stderr.write('.')
	#sys.stderr.write(' ||| '.join(candidates).encode('utf-8'))
