<div id="top"></div>

<!-- PROJECT LOGO -->
<div align="center">
  <h2 align="center">Standard Operation Procedure for Named Entity Recognition and Text Classification</h2>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#problem">Problem description</a></li>
    <li><a href="#requirement">Requirement</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#ner">Named Entity Recognition</a></li>
    <li><a href="#sentiment">Text Classification</a></li>
    
      
  </ol>
</details>

<!-- Problem description -->
## Problem
This repo implements the named entity recognition (NER) and text classification using doccano. The related instruction can be found [here](https://github.com/doccano/doccano).

<!-- Requirement -->
## Requirement 
Doccano server requires python package version at least 3.8.

<!-- Installation -->
##  Installation
Install the doccano server in local:
```shell script
conda create --name entity_matching python=3.8
conda activate entity_matching
pip3 install doccano
```

<!-- Setup -->
##  Setup
#### Terminal 1 
For the first terminals, we first need to create username and password and then call the webserver. 
For the first time running, we need to run the following commands: 
```shell script
doccano init
```
To create the username and password, we need to run the following commands:
```shell script
username=$username
password=$password
doccano createuser --username $username --password $password
```
Then we need to run the webserver using the following command, this needs to be ran every time to start the server. 
```shell script
doccano webserver --port 8000
```
#### Terminal 2
For the second terminal, we need to run the following commands for each time we are ready to do annotation task
```shell script
conda activate entity_matching
doccano task
```
Then we need to open the webpage at <http://127.0.0.1:8000/> or <http://localhost:8000>. After that, we can use the annotation tool after 
entering the username and password. 

<!-- NER -->
##  NER
<ol>
  <li>Create NER project
    <ol>
      <li>Select "Sequence Labeling" by clicking on the image. (There will be a check mark before the word "sequence labeling". </li>
      <li>Create project name, description.</li>
      <li>Click "create"</li>
    </ol>
  </li>
  <li>Import data
    <ol>
      <li>Create a txt file to be annotated.</li>
      <li>On NER project page:
        <ol>
          <li>Dataset | Actions (dropdown) | Import Dataset</li>
          <li>Select text format as TextLine</li>
          <li>Drop the txt file to the designated location</li>
          <li>Click "import"</li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Labels | Actions | Create labels:
    <ol>
          <li>configure label names, key, color. The possible label names could be: person, designation, misc, etc.</li>
           <li>Click "save".</li>
            <li>Repeat to create enough labels.</li>
    </ol>
  <li>Annotation:
    <ol>
      <li>Dataset | annotate (select any line to start)</li>
      <li>Annotate process
        <ol>
          <li>Select a word, then label option will show up. Select the label.</li>
          <li>Continue for other lines using the arrow button in the top right corner.</li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Export
    <ol>
      <li>Dataset | Actions | Export data
        <ul>
          <li>Select type JSONL</li>
          <li>Click "Export". (The file is exported to Download folder directly)</li>
        </ul>
      </li>
      <li>Open file with Notepad++ or other text editor.
        <ul>
          <li>Annotation format: id:line#, original text, label:(start index, end index, label)</li>
        </ul>
      </li>
    </ol>
  </li>
  <li>Check on other project:
    <ul>
      <li>Click Project (top right corner) to view all the project.</li>
    </ul>
  </li>
</ol>

<!-- Sentiment -->
##  Sentiment
<p>The process is similar to the NER project. The differences are:
  <ol>
    <li>Create project and select "Text classification" instead of "Sequence Labeling" .</li>
    <li>Labels are applied to the whole line. The possible labels could be "positive, negative, neutral".</li>
    <li>Annotate the whole line input to a label.</li>
  </ol>
</p>
