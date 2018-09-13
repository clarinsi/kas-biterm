# kas-biterm

Tool for extracting bilingual term pairs from translation patterns ```Slovene term (eng. English translation)``` and similar. The tool actually consists of two modules: (1) a sequence labeler which annotates terms and abbreviations in various languages in running text and (2) a term linker which links the terms and abbreviations to Slovene terms.

## Running the sequence labeler

To run the sequence labeler, the ```label.py``` script should be run, its arguments being the input file to be labeled and the model to be used for labeling. Below is a toy example of labeling the training file for the first pattern ```kas-biterm.body.ana.1.txt``` with the model trained on that same file. All information in ```kas-biterm.body.ana.1.txt``` is necessary, except for the gold annotations in the last row.

```
$ python label.py kas-biterm.body.ana.1.txt kas-biterm.body.ana.1.txt.model > kas-biterm.body.ana.1.txt.anno
```

## Running the term linker

Once terms are labeled in running text, the linker can be run on the output of the labeler.

```
$ python link.py kas-biterm.body.ana.1.txt.anno
```

The output of the script is identical to the input file, with one additional column added. This column contains at the first token of a term the token ID of the term it is the translation of.

```
999.20	napovedovanje	Ncnsa	napovedovanje	SL-TERM	SL-TERM	
999.21	z	Si	z	SL-TERM	SL-TERM	
999.22	delnim	Agpnsi	delen	SL-TERM	SL-TERM	
999.23	ujemanjem	Ncnsi	ujemanje	SL-TERM	SL-TERM	
999.24	(	Z	(	O	O	
999.25	angl.	Y	angl.	O	O	
999.26	prediction	Xf	prediction	FOR-TERM	FOR-TERM	999.20
999.27	by	Xf	by	FOR-TERM	FOR-TERM	
999.28	partial	Xf	partial	FOR-TERM	FOR-TERM	
999.29	matching	Xf	matching	FOR-TERM	FOR-TERM	
999.30	,	Z	,	O	O	
999.31	PPM	Npmsn	PPM	FOR-ABBR	FOR-ABBR	999.20
```

In this example the term 'prediction by partial matching' is linked to 'napovedavanje z delnim ujemanjem', while the 'PPM' abbreviation is linked to the same Slovene term.

## Training the sequence labeler

The training and test data is available in ```kas-biterm.body.ana.xml```. To transform the XML data into a format suitable for training the sequence labeler, the script ```transform.py``` can be called. This script produces three separate files (```kas-biterm.body.ana.1.txt``` etc.) for the three patterns used when searching for candidates in corpora. and ```kas-biterm.body.ana.txt```. The latter format is generated with the ```transform.py``` script.

To train the sequence labeler, the ```train.py``` script should be applied on one of the files prepared with the ```transform.py``` script.

```
$ python train.py kas-biterm.body.ana.1.txt
...
             precision    recall  f1-score   support

   FOR-ABBR      0.556     0.213     0.308        47
   FOR-TERM      0.784     0.881     0.830       479
          O      0.961     0.962     0.961      6660
    SL-ABBR      0.000     0.000     0.000         3
    SL-TERM      0.702     0.661     0.681       542

avg / total      0.929     0.931     0.929      7731
...

$ python train.py kas-biterm.body.ana.2.txt
...
             precision    recall  f1-score   support

   FOR-ABBR      0.875     0.359     0.509        39
   FOR-TERM      0.795     0.628     0.702       470
          O      0.935     0.980     0.957      6340
    SL-ABBR      0.000     0.000     0.000         1
    SL-TERM      0.797     0.462     0.585       433

avg / total      0.917     0.923     0.916      7283
...

$ python train.py kas-biterm.body.ana.3.txt
...
             precision    recall  f1-score   support

   FOR-TERM      0.000     0.000     0.000         8
          O      0.989     1.000     0.995      1388
    SL-TERM      1.000     0.125     0.222         8

avg / total      0.984     0.989     0.985      1404
...
```

The above reported results are obtained on 20% of data. They show that for the first two patterns reasonable results are obtained, while the third pattern does not manage to identify foreign terms and therefore is not used. After performing testing, a final model is trained on the whole of the available data.

