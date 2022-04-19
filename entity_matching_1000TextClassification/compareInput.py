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
    tableTitle = {"index": [], "entry": [], "combineScore": []}
    table = pd.DataFrame(tableTitle)
    for i in index:
        row = allScores[i].replace("\n", "").split(",")
        artistScore, trackScore = float(row[1]), float(row[2])
        combineScore = eVal.evalFunction(artistScore, trackScore, percentEval)
        pandaRow = pd.DataFrame({"index": [i], "entry": [entries[i]],
                                 "combineScore": [combineScore]})
        table = table.append(pandaRow)

        score.append(combineScore)

    score = np.array(score)

    precision, recall, thresholds = precision_recall_curve(true, score)
    thr1, thr2 = 0, 1
    for i in range(len(thresholds)):
        if recall[i] < recallThr:
            thr1 = thresholds[i]
            break
    for i in range(len(thresholds)):
        if precision[i] > precisionThr:
            thr2 = thresholds[i]
            break

    if thr1 > thr2:
        print("The chosen thresholds are not reasonable with thr1={} and thr2={}.".format(thr1, thr2))

    table1 = pd.DataFrame(tableTitle)
    table2 = pd.DataFrame(tableTitle)
    table3 = pd.DataFrame(tableTitle)
    for i in range(len(table)):
        score = table.iloc[i][2]
        if score <= thr1:
            table1 = table1.append(table.iloc[i])
        elif score >= thr2:
            table3 = table3.append(table.iloc[i])
        else:
            table2 = table2.append(table.iloc[i])


    numLabel0 = len(table1)
    numLabel1 = len(table3)
    numUncertain = len(table2)

    percentLabeled = (numLabel0 + numLabel1)/(numLabel0 + numLabel1 + numUncertain)
    print("The % of labeled items are {}.".format(percentLabeled))

    outputPandaTable(table1, "label0.csv")
    outputPandaTable(table3, "label1.csv")
    outputPandaTable(table2, "labelUncertain.csv")

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
# python .\evalFunctionForRocCurve.py --startIndex=0 --endIndex=1000 --fuzzyScoreFile="fuzzyScores.txt"
# --manualLabelFile="1000annotate.csv" -p 0.5 --combined/--no-combined
