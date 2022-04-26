"""
The goal here is to determine two thresholds to assign the data to be match (1), unmatch(0), or undetermined.

The weight has been determined from evalFunctionForRocCurve as 0.5.

The data is only the manually labeled data.

"""

import combineData
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import argparse
import evalFunctionForRocCurve as eVal
import pandas as pd


def outputPandaTable(tableName, filename):
    tableName.to_csv(r'./temp/{}'.format(filename), index=False)



def threshold(fuzzyScoreFile="fuzzyScores.txt", manualAnnotateFile="1000annotate.csv",
              percentEval=None, recallThr=0.9, precisionThr=0.9):

    # filename = "1000annotate.csv"
    df = pd.read_csv(r"{}".format(manualAnnotateFile), index_col=0)
    index = list(range(0, 1000))
    entries = [df.iloc[i][0] for i in range(len(df))]
    true = [df.iloc[i][1] for i in range(len(df))]
    true = np.array(true)

    allScores = combineData.importScore(fuzzyScoreFile)
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

    # print("The threshold setting is r={} for thr1, p={} for thr2".format(recallThr, precisionThr))
    if thr1 > thr2:
        print("The chosen thresholds are not reasonable with thr1={} and thr2={}.".format(thr1, thr2))
    else:

        print("The two thresholds are: thr1={} and thr2={}.".format(thr1, thr2))

    # directly set the thresholds:



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


    outputPandaTable(table1, "label0.csv")
    outputPandaTable(table3, "label1.csv")
    outputPandaTable(table2, "labelUncertain.csv")
    outputPandaTable(table4, "label0_incorrect.csv")
    outputPandaTable(table5, "label1_incorrect.csv")

    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    # parser.add_argument('--startIndex', type=int, required=True,
    #                     help='start index for the manually labeled data')
    # parser.add_argument('--endIndex', type=int, required=True,
    #                     help='end index for the manually labeled data')
    parser.add_argument('--fuzzyScoreFile', type=str, required=True,
                        help='path to the fuzzy score file (the default is "fuzzyScores.txt"')
    parser.add_argument('--manualLabelFile', type=str, required=True,
                        help='path to the manually labeled file (the default is "1000annotate.csv")')
    parser.add_argument('-p', '--percentForArtistScore', type=float, required=True,
                        help='set a list of weight percentage for eval function')
    # parser.add_argument('--combined', action=argparse.BooleanOptionalAction, required=True,
    #                     help='select whether to combine manual label '
    #                          'and fuzzywuzzy label with both as 0 and 100 scores'
    #                          'need to use "--combined" or "--no-combined" in the arg')
    parser.add_argument('-rt', '--recallThr', type=float, required=True,
                        help='set threshold for recall')
    parser.add_argument('-pt', '--precisionThr', type=float, required=True,
                        help='set threshold for precision')
    args = parser.parse_args()
    threshold(args.fuzzyScoreFile, args.manualLabelFile, args.percentForArtistScore, args.recallThr, args.precisionThr)

# current calling command line:
# python .\evalFunctionForRocCurve.py --fuzzyScoreFile="fuzzyScores.txt" --manualLabelFile="1000annotate.csv"
#            -p 0.5 -rt 0.9 -pt 0.9
