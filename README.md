# TM Exercise 2
Jessica Roady & Rebecka Fahrni

### Observations on Babelfy

The first thing that stood out to us was Babelfy's strange choices as to what counted as a NE. Tokens like `east`, `led`, `safety`, and `talks` seem to us to be just normal nouns, not NEs. Another noticeable issue was inconsistency in NER: some instances of `Luhansk` and `Mariupol`, for example, were recognised and correctly linked while others were not. Looking at the texts, it is not immediately clear to us why this happened -- these FNs do not appear to be in more complex linguistic structures, for example, than their TP counterparts.

Lesser-known NEs like `Serhiy Haidai`, a local political figure, were not recognised. This could be due to his relative lack of fame or to transliteration inconsistencies (he may be tagged and linked with a different Latin spelling). The same cannot be said for `President Volodymyr Zelensky`, however, as  `Volodymyr Zelensky` has a BabelNet entry with that exact spelling (albeit without the `President` part). Again, it is not clear from the surrounding linguistic structure why `Volodymyr Zelensky` was not recognised.

We were surprised that `Russian forces` was consistently correctly linked with `Russian Armed Forces`. `Ukraine's army` was not linked, however, despite the fact that a BabelNet entry for `Ukrainian Army` exists. `Russia's army` and `Ukrainian forces` also do not get recognised (do not appear in the data, manually checked), though `Russian army` interestingly does. Thus, the genitive construction seems to be a systemic issue in BabelNet NER. Other, more easily 'forgivable' FNs occur in spans like `Ukraine had already stationed its best-trained forces`, in which several tokens separate the elements of the multi-token NE.


### Observations on our annotations

Results of `IAA.py`:

```
Annotator 1:
  Precision: 0.92       Recall: 0.88	F-measure: 0.9
Annotator 2:
  Precision: 0.87	Recall: 0.91	F-measure: 0.89

TP Kappa: 0.9552
FP Kappa: 0.7277
FN Kappa: 0.8363
```

Our F-measures were almost the same, with the highest agreement on TPs and the lowest on FPs. The primary reason for this seems to be ambiguity as to whether a NE should span multiple tokens or not. Babelfy tagged `Ukraine` and `military` as two separate entities in the span `Ukraine's military`, and one of us considered this a TP whereas the other thought this was a FP because `Ukraine's military` would have been the more correct, multi-token NE. 

Another consistent point of disagreement stemmed from whether some 'normal' nouns should have been tagged by Babelfy since it tagged other, similar nouns. One of us often marked untagged nouns like `south` and `loss` as FNs because Babelfy linked nouns like `east` and `killing`, and this seemed inconsistent (especially since BabelNet entries for these exist). 