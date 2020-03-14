
Interannotator agreement study

### Appropriate interannotor agreement measure: Alpha.  

As Kappa requires the same annotators across all annotation tasks, it will not fit the case of using Amazon Mechanical Turk on Chinese Weibo data.

### Interannotator agreement scores across three languages:

lang | measure with polarity_distance2|measure with polarity_distance3(less penalty on same side polarity) 
----------|----------------------------------- |----------------------------------------------------------------
French (two annotators per task) |  0.803     |  0.813
English (two annotators per task)|       |
Chinese (three annotators per task)|   0.191    |  0.211
Overall |       |

The script that produces the agreement score across 3 languages is [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/milestone3/Interannotator_agreement_Weibo_filtered.ipynb)

### Discussion:

For the French and English tweets, the annotations process went quite well as Serena's friends and Varun's parents are very reliable. They are good in the the respective languages they annotate, followed annotation guidelines closely and are careful in delineating the subtle difference in sentiment such as "Very Positive" and "Positive".

For the Chinese Weibo posts that are put on Amazon Mechanical Turk for crowdsourcing annotations, the annotator quality is hard to ensure. Even though about 68% Weibo posts have two annotators agree on a same sentiment label, there's always a third annotator that randomly/carelessly rate it "Irrelevant" or "Neutral". Some will label many Weibo posts carries "Neutral" sentiment towards the company mentioned, while in fact they are obviously "Irrelevant", especially in the case of Facebook Weibo posts where Weibo users mentioned someone's Facebook instead of commenting on the company Facebook. 

It's hard to ensure annotator quality on Amazon Mechanical Turk. The Weibo annotation assignment requires Chinese speakers but Mechanical Turk offers very restricted worker filter. In order to use the Premium Qualification filter  "Chinese language ability: Basic", Mechanical Turk requires the assignment to hire more than 10 annotators. One workaround is to design the assignment interface to write instructions in Simplified Chinese only, so that only Chinese speakers have confidence in completing the annotations. Another quality ensurance measure is to use the basic qualifications such as HIT approval rate(e.g. set a threshold >80%), but that cannot filter out random clickers who doesn't know Chinese but want to make quite money as well. About half of the 1200(400 Weibo posts, each need 3 annotators)  annotation tasks has to be manually rejected, (with the help of velocity filter on Turk that shows WorkerID who complete an annotation taks under 10 seconds), so as to republish the tasks for others to complete.
Still, the annotation quality is not consistent across annotators. The interannotator agreement score is still low even after excluding annotations that are done within 9 seconds. 