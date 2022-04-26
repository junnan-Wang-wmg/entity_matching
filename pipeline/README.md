<div id="top"></div>

<!-- PROJECT LOGO -->
<div align="center">
  <h2 align="center">Pipeline for analyzing Wavo data </h2>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#problem">Problem description</a></li> 
    <li><a href="#data">Data description</a></li>
    <li><a href="#doccano">Manual Annotation with Doccano</a></li>
    <li><a href="#algorithm">Algorithm</a>
      <ul>
        <li><a href="#fuzzyWuzzy">Fuzzy Matching</a></li>
        <li><a href="#evalModel">Evaluation Model</a></li>
        <li><a href="#auc">Roc and Prc analysis</a></li>
        <li><a href="#check">Check original data</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- Problem description -->
## Problem description
<div id="problem"></div>
This repo is aimed to analyze the Wavo dataset. The goal is to match the entity of any input campaign name to the 
artist+track name in the database.


<!-- Data description -->
## Data description
<div id="data"></div>
This dataset is Wavo dataset. The dataset contains input as entity of the campaign names and the goal 
is to match the entity of the input campaign names to the database with artist names and track names. 


<!-- Manual Annotation with Doccano -->
##Manual Annotation with Doccano
<div id="doccano"></div>
The first step is to apply Doccano to manually annotate the data. The input for Doccano is the combination of the 
campaign name and the artist+track name. The input is converted from the original wavo data in csv. The annotation category is text classification in Doccano, and the label
would be matched(1) and unmatched(0). The final output is an CSV file containing an id (given by Doccano), data input 
(combination of campaign name and artist+track name), and the label (0 or 1).

<!-- Algorithm -->
## Algorithm
<div id="algorithm"></div>
In order to analyze the Wavo data better, fuzzy matching method is applied so that the original dataset can be trimmed 
to automatically label part of the data. Then a machine learning model would be applied to further label the remainer 
data.

## Fuzzy Matching
<div id="fuzzyWuzzy"></div>
Fuzzy score can be obtained by comparing the campaign name to the artist and track name respectively. The output for 
each comparison (either campaign name vs artist name or campaign name vs track name) would be an array of scores ranging
from 0-100. The higher the score, the more similarity between the two names.

The fuzzy score is based on partial ratio method, which means that as long as there are partially mathcing between 
two inputs, the score will be 100. In addition, the score is not case-sensitive.

## Evaluation Models
<div id="evalModel"></div>
The evaluation model is to design a function to combine the artist and track fuzzy scores. The score would be between 0 
and 1 for future purpose. The default evaluation model is to apply a weight of 0.5 for both artistScore/100 and 
trackScore/100.

The weight is a hyperparameter is determined to be 0.5 from the previous study. This hyperparameter could be adjusted.

## Roc and Prc Analysis
<div id="auc"></div>
The next step is to apply Roc and Prc analysis to compare the score from manually annotated data (from Doccanno)
and the score from fuzzy matching after being evaluated through the evaluation model. The plots for Roc and Poc 
are plotted. 

In addition, two thresholds are set in here: precision = 0.9 and recall = 0.9. This two thresholds will separate all 
the data into 3 segments: label=0, label=1, and undetermined. The unmatched data (either label=0 or label=1) are 
extracted into separate files.

## Threshold Analysis
<div id="check"></div>
The final step is to check with the original data.

From the last step, the unmatched data input will be evaluated to determine the reasons for the inconsistency between
the manual label and the fuzzy matching label. The possible reasons could be the incorrect manual annotation, or some 
other special cases.







