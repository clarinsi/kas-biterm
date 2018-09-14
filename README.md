# kas-biterm

Tool for extracting bilingual term pairs from translation patterns ```Slovene term (eng. English translation)``` and similar. The tool actually consists of two modules: (1) a sequence labeler which annotates terms and abbreviations in various languages in running text and (2) a term linker which links the terms and abbreviations to Slovene terms.

## Running the sequence labeler

To run the sequence labeler, the ```label.py``` script should be run, its argument being the model to be used for labeling. The data to be labeled should be sent to stdin, the labeled output goes to stdout. Below is a toy example of labeling the training file for the first pattern ```kas-biterm.body.ana.1.txt``` with the model trained on that same file. All information in ```kas-biterm.body.ana.1.txt``` is necessary, except for the gold annotations in the last row.

```
$ python label.py kas-biterm.body.ana.1.txt.model < kas-biterm.body.ana.1.txt > kas-biterm.body.ana.1.txt.anno
```

## Running the term linker

Once terms are labeled in running text, the linker can be run on the output of the labeler.

```
$ python link.py < kas-biterm.body.ana.1.txt.anno
```

The output of the script on stdout is identical to the input from stdin, with one additional column added. This column contains at the first token of a term the token ID of the term it is the translation of.

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

   FOR-ABBR      0.732     0.638     0.682        47
   FOR-TERM      0.808     0.914     0.858       479
          O      0.968     0.968     0.968      6660
    SL-ABBR      0.500     0.333     0.400         3
    SL-TERM      0.783     0.707     0.743       542

avg / total      0.944     0.944     0.944      7731
...

$ python train.py kas-biterm.body.ana.2.txt
...
             precision    recall  f1-score   support

   FOR-ABBR      0.913     0.538     0.677        39
   FOR-TERM      0.844     0.762     0.801       470
          O      0.958     0.979     0.969      6340
    SL-ABBR      1.000     1.000     1.000         1
    SL-TERM      0.819     0.670     0.737       433

avg / total      0.942     0.945     0.943      7283
...

$ python train.py kas-biterm.body.ana.3.txt
...
             precision    recall  f1-score   support

   FOR-TERM      0.571     0.500     0.533         8
          O      0.993     0.998     0.995      1388
    SL-TERM      1.000     0.250     0.400         8

avg / total      0.990     0.991     0.989      1404
...
```

The above reported results are obtained on 20% of data. They show that for the first two patterns reasonable results are obtained, while the third pattern does not manage to identify foreign terms and therefore is not used. After performing testing, a final model is trained on the whole of the available data.

