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

<h2 id="problem">Problem description</h2>

This repo is aimed to analyze the Wavo dataset. The goal is to match the entity of any input campaign name to the 
artist+track name in the database.

<h2 id="data">Data description</h2>

This dataset is Wavo dataset. The dataset contains input as entity of the campaign names and the goal 
is to match the entity of the input campaign names to the database with artist names and track names. 

<h2 id="doccano">Manual Annotation with Doccano</h2>

The first step is to apply Doccano to manually annotate the data. The input for Doccano is the combination of the 
campaign name and the artist+track name. The input is converted from the original wavo data in csv. The annotation category is text classification in Doccano, and the label
would be matched(1) and unmatched(0). The final output is an CSV file containing an id (given by Doccano), data input 
(combination of campaign name and artist+track name), and the label (0 or 1).

<h2 id="algorithm">Algorithm</h2>

In order to analyze the Wavo data better, fuzzy matching method is applied so that the original dataset can be trimmed 
to automatically label part of the data. Then a machine learning model would be applied to further label the remainer 
data.

<h2 id="fuzzyWuzzy">Fuzzy Matching</h2>

Fuzzy score can be obtained by comparing the campaign name to the artist and track name respectively. The output for 
each comparison (either campaign name vs artist name or campaign name vs track name) would be an array of scores ranging
from 0-100. The higher the score, the more similarity between the two names.

The fuzzy score is based on partial ratio method, which means that as long as there are partially mathcing between 
two inputs, the score will be 100. In addition, the score is not case-sensitive.

<h2 id="evalModel">Evaluation Models</h2>

The evaluation model is to design a function to combine the artist and track fuzzy scores. The score would be between 0 
and 1 for future purpose. The default evaluation model is to apply a weight of 0.5 for both artistScore/100 and 
trackScore/100.

The weight is a hyperparameter is determined to be 0.5 from the previous study. This hyperparameter could be adjusted.

<h2 id="auc">Roc and Prc Analysis</h2>

The next step is to apply Roc and Prc analysis to compare the score from manually annotated data (from Doccanno)
and the score from fuzzy matching after being evaluated through the evaluation model. The plots for Roc and Poc 
are plotted. 

In addition, two thresholds are set in here: precision = 0.9 and recall = 0.9. This two thresholds will separate all 
the data into 3 segments: label=0, label=1, and undetermined. The unmatched data (either label=0 or label=1) are 
extracted into separate files.

<h2 id="check">Threshold Analysis</h2>

The final step is to check with the original data.

From the last step, the unmatched data input will be evaluated to determine the reasons for the inconsistency between
the manual label and the fuzzy matching label. The possible reasons could be the incorrect manual annotation, or some 
other special cases.







