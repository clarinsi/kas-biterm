#!/usr/bin/python
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
  for idx,(token,msd,lemma) in enumerate(instance):
    tfeat=[]
    tfeat.append('token='+token.lower())
    tfeat.append('msd='+msd)
    tfeat.append('tag='+msd[:2])
    tfeat.append('len='+str(len(token)))
    if token.islower():
      tfeat.append('islower')
    elif token.istitle():
      tfeat.append('istitle')
    elif token.isupper():
      tfeat.append('isupper')
    #for cn in ngram(token.lower(),5):
    #  tfeat.append('ngram='+cn)
    if idx>0:
      tfeat.append('token[-1]='+instance[idx-1][0].lower())
    if idx>1:
      tfeat.append('token[-2]='+instance[idx-2][0].lower())
    if idx>2:
      tfeat.append('token[-3]='+instance[idx-3][0].lower()) 
    if idx<len(instance)-1:
      tfeat.append('token[1]='+instance[idx+1][0].lower())
    if idx<len(instance)-2:
      tfeat.append('token[2]='+instance[idx+2][0].lower())
    if idx<len(instance)-3:
      tfeat.append('token[3]='+instance[idx+3][0].lower())
    if idx>0:
      tfeat.append('tag[-1]='+instance[idx-1][1][:2])
    if idx>1:
      tfeat.append('tag[-2]='+instance[idx-2][1][:2])
    if idx>2:
      tfeat.append('tag[-3]='+instance[idx-3][1][:2])
    if idx<len(instance)-1:
      tfeat.append('tag[1]='+instance[idx+1][1][:2])
    if idx<len(instance)-2:
      tfeat.append('tag[2]='+instance[idx+2][1][:2])
    if idx<len(instance)-3:
      tfeat.append('tag[3]='+instance[idx+3][1][:2])
    """
    if idx>0:
      tfeat.append('msd[-1]='+tokens[idx-1][1])
    if idx>1:
      tfeat.append('msd[-2]='+tokens[idx-2][1])
    if idx>2:
      tfeat.append('msd[-3]='+tokens[idx-3][1])
    if idx<len(instance)-1:
      tfeat.append('msd[1]='+tokens[idx+1][1])
    if idx<len(instance)-2:
      tfeat.append('msd[2]='+tokens[idx+2][1])
    if idx<len(instance)-3:
      tfeat.append('msd[3]='+tokens[idx+3][1])
    """
    """
    for idx,val in enumerate(emb.get(token.lower(),[])):
      tfeat.append('emb'+str(idx+1)+'='+str(val))
    """
    feats.append(tfeat)
  return feats

if __name__=='__main__':
  """
  emb={}
  for line in open('vocabulary.vec'):
    line=line.decode('utf8').strip().split(' ')
    emb[line[0]]=[float(e) for e in line[1:]]
  """

  instances=[]
  for sentence in open(sys.argv[1]).read().decode('utf8').strip().split('\n\n'):
    instances.append([e.strip().split('\t') for e in sentence.split('\n')])
  random.seed(42)
  random.shuffle(instances)
  border=int(len(instances)*train_size)
  train=instances[:border]
  test=instances[border:]

  ### training

  trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
  trainer.set_params({'max_iterations':10})
  for instance in train:
    labels=[e[-1] for e in instance]
    feats=extract([(e[0],e[1],e[2]) for e in instance])
    #print feats
    #print labels
    trainer.append(feats,labels)
  trainer.train(sys.argv[1]+'.model')

  ### testing
  def transform_to_triples(seq):
    instance=['O',-1,-1]
    for idx,entry in enumerate(seq+['O']):
      if instance[0]!=entry:
        if instance[0]!='O':
          instance[2]=idx
          yield tuple(instance)
        instance[0]=entry
        instance[1]=idx

  tagger=pycrfsuite.Tagger()
  tagger.open(sys.argv[1]+'.model')
  pred=[]
  true=[]
  label_pre={}
  label_rec={}
  f=open(sys.argv[1]+'.test.out','w')
  for instance in test:
    labels=[e[-1] for e in instance]
    feats=extract([(e[0],e[1],e[2]) for e in instance])
    pred_labels=tagger.tag(feats)
    tokens=['\t'.join(e[:3]) for e in instance]
    for token,label in zip(tokens,pred_labels):
      f.write((token+'\t'+label+'\n').encode('utf8'))
    f.write('\n')
    pred.extend(pred_labels)
    true.extend(labels)
    true_triples=set(transform_to_triples(labels))
    pred_triples=set(transform_to_triples(pred_labels))
    for triple in true_triples:
      if triple[0] not in label_rec:
        label_rec[triple[0]]=[0,0.]
      label_rec[triple[0]][1]+=1
      if triple in pred_triples:
        label_rec[triple[0]][0]+=1
    for triple in pred_triples:
      if triple[0] not in label_pre:
        label_pre[triple[0]]=[0,0.]
      label_pre[triple[0]][1]+=1
      if triple in true_triples:
        label_pre[triple[0]][0]+=1
  print label_pre
  print label_rec
  from sklearn.metrics import classification_report
  print classification_report(true,pred,digits=3)

  # final training
  trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
  trainer.set_params({'max_iterations':10})
  for instance in instances:
    feats=extract([(e[0],e[1],e[2]) for e in instance])
    labels=[e[-1] for e in instance]
    #print feats
    #print labels
    trainer.append(feats,labels)
  trainer.train(sys.argv[1]+'.model')
