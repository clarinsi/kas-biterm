import sys
from lxml import etree

def process_element(child,tag='O'):
  if child.tag=='{http://www.tei-c.org/ns/1.0}w':
    sys.stdout.write((child.text+'\t'+child.get('ana')[4:]+'\t'+child.get('lemma')+'\t'+tag+'\n').encode('utf8'))
  elif child.tag=='{http://www.tei-c.org/ns/1.0}pc':
    sys.stdout.write((child.text+'\t'+child.get('ana')[4:]+'\t'+child.text+'\t'+tag+'\n').encode('utf8'))

root=etree.parse(open('kas-biterm.body.ana.xml'))
lang=None
for sentence in root.iterfind('.//{http://www.tei-c.org/ns/1.0}s'):
  for child in sentence:
    process_element(child)
    if child.tag=='{http://www.tei-c.org/ns/1.0}term':
      lang=child.get('{http://www.w3.org/XML/1998/namespace}lang')
      for grandchild in child:
        process_element(grandchild,lang.upper())
      lang=None
  sys.stdout.write('\n')
        