import sys
import cPickle as pickle
import pycrfsuite
import random
train_size=0.8

def ngram(token,length=3):
  token='^'+token+'$'
  for idx in range(len(token)-length-1):
    yield token[idx:idx+length]

def extract(instance):
  feats=[]
  labels=[]
  tokens=[e.split('\t') for e in instance.split('\n')]
  for idx,(token,msd,lemma,label) in enumerate(tokens):
    tfeat=[]
    labels.append(label)
    tfeat.append('token='+token.lower())
    tfeat.append('msd='+msd)
    tfeat.append('tag='+msd[:2])
    for cn in ngram(token.lower(),4):
      tfeat.append('ngram='+cn)
    if idx>0:
      tfeat.append('token[-1]='+tokens[idx-1][0].lower())
    if idx>1:
      tfeat.append('token[-2]='+tokens[idx-2][0].lower())
    if idx>2:
      tfeat.append('token[-3]='+tokens[idx-3][0].lower()) 
    if idx<len(tokens)-1:
      tfeat.append('token[1]='+tokens[idx+1][0].lower())
    if idx<len(tokens)-2:
      tfeat.append('token[2]='+tokens[idx+2][0].lower())
    if idx<len(tokens)-3:
      tfeat.append('token[3]='+tokens[idx+3][0].lower())
    if idx>0:
      tfeat.append('msd[-1]='+tokens[idx-1][1])
    if idx>1:
      tfeat.append('msd[-2]='+tokens[idx-2][1])
    if idx>2:
      tfeat.append('msd[-3]='+tokens[idx-3][1])
    if idx<len(tokens)-1:
      tfeat.append('msd[1]='+tokens[idx+1][1])
    if idx<len(tokens)-2:
      tfeat.append('msd[2]='+tokens[idx+2][1])
    if idx<len(tokens)-3:
      tfeat.append('msd[3]='+tokens[idx+3][1])
    """
    if idx>0:
      tfeat.append('tag[-1]='+tokens[idx-1][1][:2])
    if idx>1:
      tfeat.append('tag[-2]='+tokens[idx-2][1][:2])
    if idx>2:
      tfeat.append('tag[-3]='+tokens[idx-3][1][:2])
    if idx<len(tokens)-1:
      tfeat.append('tag[1]='+tokens[idx+1][1][:2])
    if idx<len(tokens)-2:
      tfeat.append('tag[2]='+tokens[idx+2][1][:2])
    if idx<len(tokens)-3:
      tfeat.append('tag[3]='+tokens[idx+3][1][:2])
    if token.islower():
      tfeat.append('islower')
    elif token.istitle():
      tfeat.append('istitle')
    elif token.isupper():
      tfeat.append('isupper')
    for idx,val in enumerate(emb.get(token.lower(),[])):
      tfeat.append('emb'+str(idx+1)+'='+str(val))
    """
    feats.append(tfeat)
  return feats,labels

emb={}
for line in open('vocabulary.vec'):
  line=line.decode('utf8').strip().split(' ')
  emb[line[0]]=[float(e) for e in line[1:]]

instances=open('kas-biterm.body.ana.txt').read().decode('utf8').strip().split('\n\n')
random.seed(42)
random.shuffle(instances)
border=int(len(instances)*train_size)
train=instances[:border]
test=instances[border:]

### training

trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
trainer.set_params({'max_iterations':10})
for instance in train:
  feats,labels=extract(instance)
  #print feats
  #print labels
  trainer.append(feats,labels)
trainer.train('model')

### testing
tagger=pycrfsuite.Tagger()
tagger.open('model')
pred=[]
true=[]
for instance in test:
  feats,labels=extract(instance)
  pred_labels=tagger.tag(feats)
  pred.extend(pred_labels)
  true.extend(labels)
from sklearn.metrics import classification_report
print classification_report(true,pred,digits=3)