<div id="top"></div>

<!-- PROJECT LOGO -->
<div align="center">
  <h2 align="center">Pipeline for analyzing Wavo data </h2>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#problem">Problem Description</a></li> 
    <li><a href="#data">Data Description</a></li>
    <li><a href="#algorithm">Algorithm</a>
      <ul>
        <li><a href="#doccano">Manual Annotation with Doccano</a></li>
        <li><a href="#fuzzyWuzzy">Fuzzy Matching</a></li>
        <li><a href="#evalModel">Evaluation Model and Roc&Prc Analysis</a></li>
        <li><a href="#check">Threshold Analysis with the Original Data</a></li>
      </ul>
    </li>
    <li><a href="#note">Final Note</a>
  </ol>
</details>

<h2 id="problem">Problem description</h2>

This repo is aimed to analyze the Wavo dataset. The goal is to match the entity of any input campaign name to the 
artist+track name in the database.

<h2 id="data">Data description</h2>

This dataset is Wavo dataset. The dataset contains input as entity of the campaign names and the goal 
is to match the entity of the input campaign names to the database with artist names and track names. 

<h2 id="algorithm">Algorithm</h2>

In order to analyze the Wavo data better, fuzzy matching method is applied so that the original dataset can be trimmed 
to automatically label part of the data. Then a machine learning model would be applied to further label the remainer 
data.

<h2 id="doccano">Manual Annotation with Doccano</h2>

The first step is to apply Doccano to manually annotate the data. The input for Doccano is the combination of the 
campaign name and the artist+track name. The input is converted from the original wavo data in csv. The annotation category is text classification in Doccano, and the label
would be matched(1) and unmatched(0). The final output is an CSV file containing an id (given by Doccano), data input 
(combination of campaign name and artist+track name), and the label (0 or 1).

Process:
1. Coding: (open command prompt in "app" directory)
```shell script
python dataConverter.py -t "../data/extract.txt"  -s "../data/matching_data.csv" --startIndex 0 --endIndex 1000
```
The output file is the extracted data containing the campaign name, artist name, and track name in each row. 
The output file is saved in "data" directory.

2. Manual annotation:
    Currently, the pipeline is setup in a way that we subset the entire data. However, pre-process can be taken separately
    to avoid annotating entities with either a too high or low score.

    The next step is to import the data into Doccano and perform manual annotation. The manual annotation result is a 
csv file containing combined entry (campaign, artist, and track names) and the annotated label (1 for matched, 
0 for unmatched)
    To run Doccano, two command prompts should be open:
Command line setup1:
```shell script
doccano webserver --port 8000
```
Command line setup2:
```shell script
doccano task
```
   For more details, please check the "Doccano Instruction.md" file. Note that the label for matched is set to 1, and 
   for unmatched is set to 0. After finishing the manual annotation, output the result as csv file and transfer to the 
   data directory here. My naming here is "1000annotate.csv".


<h2 id="fuzzyWuzzy">Fuzzy Matching</h2>

Fuzzy score can be obtained by comparing the campaign name to the artist and track name respectively. The output for 
each comparison (either campaign name vs artist name or campaign name vs track name) would be an array of scores ranging
from 0-100. The higher the score, the more similarity between the two names.

The fuzzy score is based on partial ratio method, which means that as long as there are partially mathcing between 
two inputs, the score will be 100. In addition, the score is not case-sensitive.

Process:

```shell script
python fuzzyWuzzy.py --file "../data/matching_data.csv" --output "../data/fuzzyScores.txt" --startIndex 0 --endIndex 1000 --preprocess
```
The code above set preprocessing to be true. If you do not want preprocessing, simply change "--process" 
to "--no-process". The output file contains the index, artistScore, and trackScore. The file is saved to 
the "data" directory.


<h2 id="evalModel">Evaluation Model and Roc&Prc Analysis</h2>

The evaluation model is to design a function to combine the artist and track fuzzy scores. The score would be between 0 
and 1 for future purpose. The default evaluation model is to apply a weight of 0.5 for both artistScore/100 and 
trackScore/100.

The weight is a hyperparameter is determined to be 0.5 from the previous study. Here is to optimize this 
weight hyperpameter. The ROC and PRC analysis are performed in here. 

Process:

```shell script
python evalFunctionAndAUC.py -f "../data/fuzzyScores_0-1000.txt"   -m "../data/0-1000data/1000annotate.csv" -p 0.2 0.4 0.5 0.6 0.8 -save "temp"
```
The default coding above obtain the fuzzy score and manual annotation result from step2 and step 1, respectively. 
The filenames should be adjusted. Then weight percentages that are evaluated should be attached after "-p".
"-save" specifies where to save the output files. Typically, set "save" as "temp", and move the result to data 
after checking.
The output would be 2 png files:
1. roc curve of all the percentEval values
2. prc curve of all the percentEval values
The console will show the best weight percentage based on the auc scores. The previous study shows that 0.5 is the 
optimal weight percentage.

Then transfer the results from "temp" directory to "data" directory.

<h2 id="check">Threshold Analysis with Original Data</h2>

The final step is to check the separation of the data based on the thresholds that user determined. 

Process:

```shell script
python compareInput.py -f "../data/fuzzyScores_0-1000.txt" -m "../data/1000annotate.csv" -p 0.5 -rt 0.97 -pt 0.9 -save "temp"
```
The default coding above obtain the fuzzy score and manual annotation result from step2 and step 1, respectively. 
The filenames should be adjusted. The optimal weight percentage is set to "-p 0.5". This could be adjusted based on the previous result. The threshold 
"rt" and "pt" can also be adjusted to better separate the data.
"-save" specifies where to save the output files. Typically, set "save" as "temp", and move the result to data 
after checking.

The output would be 5 csv files with each file containing different segments of the data: 

   **index, entry, combineScore, trueLabel.**

1. data with label=0
2. data with label=1
3. data with label=undetermined
4. incorrect data with label=0 (true label=1)
5. incorrect data with label=1 (true label=0)

Then transfer the results from "temp" directory to "data" directory.

Then the incorrect labels can be easily viewed in the two incorrect data csv files. The reasons for the 
inconsistency between manual annotation and fuzzy wuzzy score can be summarized. 
In addition, the thresholds can be adjusted by chaning "-rt" and "-pt" to obtain better separation of data.


From the last step, the unmatched data input will be evaluated to determine the reasons for the inconsistency between
the manual label and the fuzzy matching label. The possible reasons could be the incorrect manual annotation, or some 
other special cases.

<h2 id="note">Final Note</h2>
The code above directly saved the data files in data directory. In order to more organized to store the data, the 
data directory is now with subdirectory, such as "0-1000data" subdirectory. The information is simply moved from the 
data directory into the subdirectory.





