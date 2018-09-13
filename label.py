import sys
import cPickle as pickle
import pycrfsuite
import random
train_size=0.8

from train import extract

instances=[]
for sentence in open(sys.argv[1]).read().decode('utf8').strip().split('\n\n'):
  instances.append([e.strip().split('\t') for e in sentence.split('\n')])

tagger=pycrfsuite.Tagger()
tagger.open(sys.argv[2])
pred=[]
for instance in instances:
  labels=[e[-1] for e in instance]
  feats=extract([(e[0],e[1],e[2]) for e in instance])
  pred_labels=tagger.tag(feats)
  for token,label in zip(instance,pred_labels):
    sys.stdout.write(('\t'.join(token)+'\t'+label+'\n').encode('utf8'))
  sys.stdout.write('\n')
