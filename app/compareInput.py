"""
compareInput.py
Determine two thresholds to assign the data to be match (1), unmatch(0), or undetermined. The thresholds are determined
by the input precision and recall threshold.

Example:
    input: r=0.97, p=0.9
    output: the dataset is divided into three categories: label=0, label=1, and label=undetermined

"""

import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import argparse
import evalFunctionAndAUC as eVal
import pandas as pd
import re


# output panda table to be in format csv.
def outputPandaTable(tableName, filename, saveToFile="temp"):
    tableName.to_csv(r'../{}/{}'.format(saveToFile, filename), index=False)


# # apply the weight percentage to artistScore and trackScore. The result combination score is between 0 and 1.
# def evalFunction(artistScore, trackScore, percentageForArtistScore=0.5):
#     artistScoreRatio = artistScore / 100
#     trackScoreRatio = trackScore / 100
#     score = percentageForArtistScore * artistScoreRatio + (1 - percentageForArtistScore) * trackScoreRatio
#     return score


# # import a txt file. Here the goal is to import that fuzzyScore file
# def importScore(filename):
#     f = open(filename, "r")
#     lines = f.readlines()
#     lines = lines[1:]  # skip the title line
#     return lines


def threshold(fuzzyScoreFile, manualAnnotateFile="1000annotate.csv",
              percentEval=None, recallThr=0.9, precisionThr=0.9, saveToFile="temp"):
    """

    :param fuzzyScoreFile: the txt file containing all the fuzzy score obtained by using fuzzyWuzzy.py
    :param manualAnnotateFile: the csv file containing all the annotated data. The file is obtained after finishing
                                the doccano annotation
    :param percentEval: float between (0,1), weight percentage for artist name to insert into the evaluation function.
                        The weight percentage for track name is (1-percentEval).
    :param recallThr: float between (0,1), the threshold for recall to set the lower threshold
    :param precisionThr:  float between (0,1), the threshold for precision to set the higher threshold
    :param saveToFile: the directory path (not the file path) to store the result files.
                            The options are: "temp", "data/dirname", etc.
    :return: 5 csv files containing different segments of the data. Each file contains data in each row as:
                    index, entry, combineScore, trueLabel.
                1. data with label=0
                2. data with label=1
                3. data with label=undetermine
                4. incorrect data with label=0 (true label=1)
                5. incorrect data with label=1 (true label=0)

            console output:
                1. two thresholds
                2. % of data labeled as either 0 or 1
                3. accuracy for label=0 and label=1, respectively
    """

    df = pd.read_csv(r"{}".format(manualAnnotateFile), index_col=0)
    splitName = re.split('-|_|\.',fuzzyScoreFile)   # the fuzzyScoreFile naming must end with format like "_0-1000.txt"
    startIndex = int(splitName[-3])
    endIndex = int(splitName[-2])
    # index = list(range(startIndex, endIndex))
    index = list(range(0, endIndex - startIndex))
    entries = [df.iloc[i][0] for i in range(len(df))]
    true = [df.iloc[i][1] for i in range(len(df))]
    true = np.array(true)

    allScores = eVal.importScore(fuzzyScoreFile)
    score = []
    tableTitle = {"index": [], "entry": [], "combineScore": [], "trueLabel":[]}
    table = pd.DataFrame(tableTitle)
    for i in index:
        row = allScores[i].replace("\n", "").split(",")
        artistScore, trackScore = float(row[1]), float(row[2])
        combineScore = eVal.evalFunction(artistScore, trackScore, percentEval)
        pandaRow = pd.DataFrame({"index": [i], "entry": [entries[i]],
                                 "combineScore": [combineScore], "trueLabel": [true[i]]})
        table = table.append(pandaRow)

        score.append(combineScore)

    score = np.array(score)

    precision, recall, thresholds = precision_recall_curve(true, score)
    thr1, thr2 = 0, 1
    for i in range(len(thresholds)):
        if recall[i] < recallThr:
            thr1 = thresholds[i-1]
            break
    for i in range(len(thresholds)):
        if precision[i] > precisionThr:
            thr2 = thresholds[i-1]
            break

    if thr1 > thr2:
        print("The chosen thresholds are not reasonable with thr1={} and thr2={}.".format(thr1, thr2))
    else:

        print("The two thresholds are: thr1={} and thr2={}.".format(thr1, thr2))

    # directly set the thresholds??

    table1 = pd.DataFrame(tableTitle)
    table2 = pd.DataFrame(tableTitle)
    table3 = pd.DataFrame(tableTitle)

    count1, count2, count3 = 0, 0, 0

    table4 = pd.DataFrame(tableTitle)
    table5 = pd.DataFrame(tableTitle)

    for i in range(len(table)):
        score = table.iloc[i][2]
        if score <= thr1:
            table1 = table1.append(table.iloc[i])
            trueLabel = table.iloc[i][3]
            if trueLabel == 0:
                count1 += 1
            else:
                table4 = table4.append(table.iloc[i])  # summarize incorrect labels in a separate table
        elif score >= thr2:
            table3 = table3.append(table.iloc[i])
            trueLabel = table.iloc[i][3]
            if trueLabel == 1:
                count3 += 1
            else:
                table5 = table5.append(table.iloc[i])  # summarize incorrect labels in a separate table
        else:
            table2 = table2.append(table.iloc[i])


    numLabel0 = len(table1)
    numLabel1 = len(table3)
    numUncertain = len(table2)

    percentLabeled = (numLabel0 + numLabel1)/(numLabel0 + numLabel1 + numUncertain)
    print("The % of labeled items are {}.".format(percentLabeled))

    acc1 = count1/len(table1)
    acc3 = count3/len(table3)

    print("The accuracy for label as 0 is {} ({}/{})\n "
          "for label as 1 is {} ({}/{}).".format(acc1, count1, len(table1), acc3, count3, len(table3)))


    outputPandaTable(table1, "label0.csv", saveToFile)
    outputPandaTable(table3, "label1.csv", saveToFile)
    outputPandaTable(table2, "labelUncertain.csv", saveToFile)
    outputPandaTable(table4, "label0_incorrect.csv", saveToFile)
    outputPandaTable(table5, "label1_incorrect.csv", saveToFile)

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    parser.add_argument('-f', '--fuzzyScoreFile', type=str, required=True,
                        help='path to the fuzzy score file (the default is "fuzzyScores.txt"')
    parser.add_argument('-m', '--manualLabelFile', type=str, required=True,
                        help='path to the manually labeled file (the default is "1000annotate.csv")')
    parser.add_argument('-p', '--percentForArtistScore', type=float, required=True,
                        help='set a list of weight percentage for eval function')
    parser.add_argument('-rt', '--recallThr', type=float, required=True,
                        help='set threshold for recall')
    parser.add_argument('-pt', '--precisionThr', type=float, required=True,
                        help='set threshold for precision')
    parser.add_argument('-save', '--saveToFile', type=str, required=True,
                        help='save files to (either "temp" or "data/filename")')
    args = parser.parse_args()
    threshold(args.fuzzyScoreFile, args.manualLabelFile, args.percentForArtistScore, args.recallThr,
              args.precisionThr, args.saveToFile)

