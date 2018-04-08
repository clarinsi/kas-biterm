# kas-biterm
Tool for extracting bilingual term pairs from translation patterns (eng. )

The training and test data is available in ```kas-biterm.body.ana.xml``` and ```kas-biterm.body.ana.txt```. The latter format is generated with the ```transform.py``` script.

Training and testing, together with the fixed data split, is performed with the ```train.py``` script.

The results are the following:

```
             precision    recall  f1-score   support

         EN      0.827     0.818     0.823       890
          O      0.960     0.981     0.970     12798
         SL      0.865     0.659     0.748       994
        UND      1.000     0.211     0.348        38

avg / total      0.946     0.947     0.945     14720
```
