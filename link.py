import sys
sentence=[]
def min_distance(term1,term2):
  start1,end1=term1[0][-1],term1[-1][-1]
  start2,end2=term2[0][-1],term2[-1][-1]
  return min(abs(start1-end2),abs(start2-end1))

for line in sys.stdin:
  if line.strip()=='':
    terms={'SL-TERM':[],'FOR-TERM':[],'SL-ABBR':[],'FOR-ABBR':[]}
    term=[]
    for idx,token in enumerate(sentence):
      if not token[-1].startswith('O'):
        if len(term)>0:
          #print term[-1][0][-1],token[-1]
          if term[-1][0][-1]!=token[-1]:
            terms[term[0][0][-1]].append(tuple(term))
            term=[]
        term.append((token,idx))
      else:
        if len(term)>0:
          terms[term[0][0][-1]].append(tuple(term))
          term=[]
    if len(term)>0:
      terms[term[0][0][-1]].append(tuple(term))
    #print sentence
    abbr=len(terms['SL-TERM'])==0
    if abbr:
      main=dict([(tuple(e),[]) for e in terms['SL-ABBR']])
      main=terms['SL-ABBR']
    else:
      #main=dict([(tuple(e),[]) for e in terms['SL-TERM']])
      main=terms['SL-TERM']
    #print terms
    if not abbr:
      categories=('FOR-TERM','FOR-ABBR','SL-ABBR')
    else:
      categories=('FOR-TERM','FOR-ABBR')
    candidates=[]
    for category in categories:
      for candidate in terms[category]:
        for term in main:
          #print term,candidate
          candidates.append((min_distance(term,candidate),term[-1][-1],term,candidate))
    #print sorted(candidates)
    taken=set()
    mappings={}
    for distance,start,term,candidate in sorted(candidates):
      if candidate in taken or term in taken:
        continue
      taken.add(candidate)
      #taken.add(term)
      #print ' '.join([e[0][0] for e in term]),'|',' '.join([e[0][0] for e in candidate]),'|',distance
      mappings[candidate[0][0][0]]=term[0][0][0]
    for token in sentence:
      tid=token[0]
      sys.stdout.write('\t'.join(token)+'\t'+mappings.get(tid,'')+'\n')
    sys.stdout.write('\n')
    sentence=[]
    continue
  line=line.strip().split('\t')
  sentence.append(tuple(line))
