# TM Exercise 2
Jessica Roady & Rebecka Fahrni

### Observations on Babelfy

The first thing that stood out to us was Babelfy's strange choices as to what counted as a NE. Tokens like `east`, `led`, `safety`, and `talks` seem to us to be just normal nouns, not NEs. 

Another noticeable issue was inconsistency in NER - some instances of `Luhansk` and `Mariupol`, for example, were recognised and correctly linked while others were not. Looking at the texts, it is not immediately clear to us why this happened - these FNs do not appear to be in more complex linguistic structures, for example, than their TP counterparts.

Lesser-known NEs like `Serhiy Haidai`, a local political figure, were not recognised. This could be due to his lack of fame or to transliteration inconsistencies (he may be tagged and linked with a different Latin spelling). The same cannot be said for `President Volodymyr Zelensky`, however, as  `Volodymyr Zelensky` has a BabelNet entry with that exact spelling (albeit without the `President` part). Again, it is not clear from the surrounding linguistic structure why this was the case.

We were surprised that `Russian forces` was consistently correctly linked with `Russian Armed Forces`. The genitive construction `Ukraine's army` appears in the data and is not linked, despite the fact that `Ukrainian Army` has a BabelNet entry with several synonyms. On the other hand, `Ukrainian forces` does not get recognised (manually checked). `Russia's army` (manually checked) also does get recognised, though `Russian army` interestingly does. The genitive construction in this case thus seems to be a systemic issue in BabelNet NER. Other, more easily 'forgivable' FNs occur in spans like `Ukraine had already stationed its best-trained forces`, in which several tokens separate the elements of the multi-token NE.


### Observations on our annotations



- F-measures are basically the same
- agree the most on TPs
- agree the least on FPs:
  - whether NEs should be multi-token or not
  - whether normal nouns should have been found by Babelfy since it tags other normal nouns