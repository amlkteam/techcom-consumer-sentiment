
# Interannotator agreement study

### Appropriate interannotor agreement measure we picked: Alpha  

As Kappa requires the same annotators across all annotation tasks, it will not fit the case of using Amazon Mechanical Turk on Chinese Weibo data. Alpha is fine to use for both cases of 1. same annotators across all tasks and 2. different combinations of annotators across different tasks. 

### Interannotator agreement scores across three languages:

Language | measure with polarity_distance2|
----------|----------------------------------- |
French (two annotators per task) |  0.803     | 
English (two annotators per task)|   0.7805    |
Chinese (three annotators per task)|   0.191    | 
Overall (taking an average of 3 scores above) |   0.5915    |

The script that produces the agreement score across 3 languages is [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/milestone3/Interannotator_agreement_Weibo_filtered.ipynb)

### Discussion:

For the French and English tweets, the annotations processes went quite well as Serena's friends and Varun's parents are very reliable. They are good in the the respective languages they annotate, followed annotation guidelines closely and are careful in distinguishing the subtle difference in sentiment such as "Very Positive" and "Positive".

For the Chinese Weibo posts that are put on Amazon Mechanical Turk for crowdsourcing annotations, the annotator quality is hard to ensure. Even though about 68% Weibo posts have two annotators agree on a same sentiment label, there's always a third annotator that randomly/carelessly rate it "Irrelevant" or "Neutral". Some will label many Weibo posts as carrying "Neutral" sentiment towards the company mentioned, while in fact they are obviously "Irrelevant" to the company, especially in the case of Facebook, where Weibo users mentioned someone's Facebook instead of commenting on the Facebook company or its products. 

It's hard to ensure annotator quality on Amazon Mechanical Turk. The Weibo annotation assignment requires Chinese speakers but Mechanical Turk offers very restricted worker filter. In order to use the Premium Qualification filter  "Chinese language ability: Basic", Mechanical Turk requires the assignment to hire more than 10 annotators. One workaround to ensure quality taken to write the assignment interface entirely in Simplified Chinese, so that only Chinese speakers have confidence in completing the annotations. Another quality ensurance measure adopted is to use the basic qualifications such as HIT approval rate(e.g. set a threshold >80%), but that also cannot completely filter out random clickers who don't know Chinese but want to make quick money(Turk has an auto-approval-within-3-days mechanism). About half of the 1200(400 Weibo posts, each need 3 annotators) annotation tasks have been rejected manually, with the help of a velocity filter on Turk that shows WorkerID who completed an annotation task within 10 seconds, so as to republish the tasks for others to complete. Still, the annotation quality is not consistent across annotators. The interannotator agreement score is still low at 0.19 even after excluding annotations that are done within 9 seconds. 