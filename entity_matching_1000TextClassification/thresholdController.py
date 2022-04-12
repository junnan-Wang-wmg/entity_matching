"""
The goal is to adjust the threshold to fuzzy score to find the threshold with good accuracy
and proper removal percentage of data.

input:
    1. fuzzyScores.txt - obtained from fuzzyWuzzy.py result
        - contains the artistScore and trackScore for all the input
    2. 1000annotate.csv
        - from doccano annotation for the first 1000 data points

output:
    1. thresholdAdj.txt
        - matching score is set as follows:
            if both artistScore and trackScore are 100, then matching score = 1
            if artistScore or trackScore is below the threshold, then matching score = 0
        - here the threshold is explored in 50 - 80 scores with an increment of 5 for both scores.

comment:
    The result suggests that the correct rate is still > 96% with both threshold set as 100. This means
    that the fuzzy wuzzy  itself is already capable of providing an accuracy of 96% in assigning labels.


"""



import pandas as pd


# import score file
def importScore(filename="fuzzyScoresAll.txt"):
    f = open(filename, "r")
    lines = f.readlines()
    lines = lines[1:]  # skip the title line
    return lines


# import label file
def importLabel(filename="1000annotate.csv"):
    df = pd.read_csv(r"{}".format(filename), index_col=0)  # empty lines will be omitted
    return df


# Set threshold to compare:
def thresholdDetermine(scores, labels, artistScoreThreshold, trackScoreThreshold):
    numAnnotatedLabels = len(labels)
    correct = 0
    incorrect = 0
    undetermined = 0

    # adjust scores from string input
    for i in range(numAnnotatedLabels):
        row = scores[i].replace("\n", "").split(",")  # index, artistScore, trackScore, previousAssign
        artistScore = float(row[1])
        trackScore = float(row[2])
        trueLabel = labels.iloc[i][1]  # combo entry, trueLabel in each labelData row
        if artistScore == 100 and trackScore == 100:  # only fuzzy score = 100 are considered matching
            if trueLabel == 1:
                correct += 1
            else:
                incorrect += 1
        elif 0 <= artistScore <= artistScoreThreshold and 0 <= trackScore <= trackScoreThreshold:
            if trueLabel == 0:
                correct += 1
            else:
                incorrect += 1
        else:
            undetermined += 1

    correctRate = correct / (correct + incorrect)
    determinedPercent = 1 - undetermined / numAnnotatedLabels

    return correctRate, determinedPercent


def adjustThreshold(filename, scores, labels):
    file = open("{}".format(filename), "w")
    file.close()  # clear all the pre-existed content

    file = open("{}".format(filename), 'a', encoding='utf-8')  # append mode, encoding is necessary!
    file.writelines("artistThreshold, trackThreshold, correctRate, determinedPercent\n")
    for artistThreshold in range(50, 101, 5):
        for trackThreshold in range(50, 101, 5):
            correctRate, determinedPercent = thresholdDetermine(scores, labels, artistThreshold, trackThreshold)
            file.writelines("{},{},{},{}\n".format(artistThreshold, trackThreshold, correctRate, determinedPercent))
    file.close()


scoreFile = "fuzzyScores.txt"
labelFile = "1000annotate.csv"

scoreData = importScore(scoreFile)  # score here contains all the scores (256,063 data)
labelData = importLabel(labelFile)  # label here contains 1000 data (from 0-1000 now)

# output data with threshold 50 - 80 for both score and label data with an increment of 5
fileOutput = "thresholdAdj.txt"
adjustThreshold(fileOutput, scoreData, labelData)

print(labelData["label"].value_counts())
