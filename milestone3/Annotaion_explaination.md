# Annotation + explanation + code

## Annotation Files

### English Annotation Files

Annotator 1 files can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/tree/master/data/English_annot1)

Combined Annotator 1 files can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/data/comb_annot1_eng.xlsx)

Annotator 2 files can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/tree/master/data/English_annot2)

Combined Annotator 2 files can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/data/comb_annot2_eng.xlsx)

#### Combined best English Annotation file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/data/final_annotations_english.csv)

### French Annotation Files

Annotator 1 file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/data/to_annotate_joanna_finished.csv)

Annotator 2 file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/data/to_annotate_molly_finished.csv)

#### Combined best French Annotation file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/milestone3/final_anotations_french.csv)

### Chinese Annotation Files

Annotator file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/data/ChineseWeiboCorpus/MTurk_Batch_3948609_full2074_results.csv)

#### Combined best Chinese Annotation file can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/data/ChineseWeiboCorpus/Weibo_final_annotations.csv)

## Code

Code used to prepare Chinese annotation can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/milestone3/M_Turk_csvtransform.ipynb)

Code used to convert the raw annotation into the final annotation can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/milestone3/Weibo_prepare_final_annotations.ipynb) and [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/master/milestone3/combining_annotation_files.ipynb)

## Discussion

The main problem our annotators faced was distinguishing between the annotation categories. They had a diffucult time deciding if a tweet was Positive or Very Positive or if it was Negative or Very Negative. The annotators mentioned that even when it came to deciding between Neutral and Irrelevant there was some confusion. For example, if there was a tweet saying "$200 Amazon gift card. Click here #Amazon". It was hard for some annotators to decide if the tweets like the one above were Neutral or Irrelevant.

When it came to Amazon Mechanical Turk, it was difficult to ensure annotator quality. The annotation assignment required Chinese speakers but the Premium Qualification on Mechanical Turk required the assignment to have more than 10 annotators in order to use that Premium Qualification requirement. Therefore our workaround was to design the assignment interface to write instructions in Simplified Chinese only, so that only Chinese speakers would have confidence in completing the annotations. Yet, the basic qualifications such as HIT approval rate(e.g. set a threshold >80%) could not filter out random clickers who did not know Chinese. We had to reject about half of the 1200 annotation tasks, so as to republish the relevant tasks.
