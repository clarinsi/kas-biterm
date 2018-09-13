import sys
from lxml import etree

def process_element(child,tag='O'):
  global sid
  global tid
  if child.tag=='{http://www.tei-c.org/ns/1.0}w':
    tid+=1
    f.write((str(sid+1)+'.'+str(tid)+'\t'+child.text+'\t'+child.get('ana')[4:]+'\t'+child.get('lemma')+'\t'+tag+'\n').encode('utf8'))
  elif child.tag=='{http://www.tei-c.org/ns/1.0}pc':
    tid+=1
    f.write((str(sid+1)+'.'+str(tid)+'\t'+child.text+'\t'+child.get('ana')[4:]+'\t'+child.text+'\t'+tag+'\n').encode('utf8'))

root=etree.parse(open('kas-biterm.body.ana.xml'))
lang=None
sent=''
i=0
for div in root.iterfind('.//{http://www.tei-c.org/ns/1.0}div'):
  pattern=div.get('{http://www.w3.org/XML/1998/namespace}n')
  i+=1
  f=open('kas-biterm.body.ana.'+str(i)+'.txt','w')
  for sid,sentence in enumerate(div.iterfind('.//{http://www.tei-c.org/ns/1.0}s')):
    tid=0
    for child in sentence:
      process_element(child)
      if child.tag=='{http://www.tei-c.org/ns/1.0}term':
        lang=child.get('{http://www.w3.org/XML/1998/namespace}lang')
        if lang in ('en','und'):
          lang='for'
        for grandchild in child:
          process_element(grandchild,lang.upper()+'-TERM')
        lang=None
      elif child.tag=='{http://www.tei-c.org/ns/1.0}abbr':
        lang=child.get('{http://www.w3.org/XML/1998/namespace}lang')
        if lang in ('en','und'):
          lang='for'
        for grandchild in child:
          process_element(grandchild,lang.upper()+'-ABBR')
        lang=None
    f.write('\n')
