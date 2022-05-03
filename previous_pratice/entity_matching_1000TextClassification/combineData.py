"""
This file is aimed at obtaining all the ground truth values:
1. manually labeled data (.csv file)
2. the data that are with both score 100 and score 0 for artist and track name (.txt file)
"""

import pandas as pd
import argparse


# import score file into a list
def importScore(filename="fuzzyScores.txt"):
    f = open(filename, "r")
    lines = f.readlines()
    lines = lines[1:]  # skip the title line
    return lines


# Extract the fuzzy scores with both score=100 or 0
def extractFuzzyScore(filename="fuzzyScores.txt"):
    allScores = importScore(filename)
    indexList = []
    for scoreRow in allScores:
        sepScoreRow = scoreRow.replace("\n", "").split(",")
        index, artistScore, trackScore = float(sepScoreRow[0]), float(sepScoreRow[1]), float(sepScoreRow[2])
        if artistScore == 100 and trackScore == 100:
            indexList.append([int(index), 1])  # set label=1 for this index
        elif artistScore == 0 and trackScore == 0:
            indexList.append([int(index), 0])  # set label=0 for this index
    return indexList


# import label file
def importLabel(startLabelIndex, endLabelIndex, filename="1000annotate.csv"):
    df = pd.read_csv(r"{}".format(filename), index_col=0)  # empty lines will be omitted
    labeledScore = []
    for index in range(len(df)):
        labeledScore.append([index + startLabelIndex, df.iloc[index][1]])
    return labeledScore


def combineData(manualStartIndex, manualEndIndex,
                fuzzyScoreFile="fuzzyScores.txt", manualAnnotateFile="1000annotate.csv", isCombined=True):
    fuzzyLabelWithCertain = extractFuzzyScore(fuzzyScoreFile)
    manualLabel = importLabel(manualStartIndex, manualEndIndex, manualAnnotateFile)

    # avoid the overlap:
    fuzzyLabelNoOverlap = fuzzyLabelWithCertain[0:manualStartIndex] + fuzzyLabelWithCertain[manualEndIndex:]

    # combine:
    combineGroundTruthLabel = (manualLabel + fuzzyLabelNoOverlap) if isCombined else manualLabel

    return combineGroundTruthLabel


# fuzzyScoreFilename = "fuzzyScores.txt"
# labelScoreFilename = "1000annotate.csv"
# manualLabelStartIndex = 0
# manualLabelEndIndex = 1000
#
# groundTruth = combineData(manualLabelStartIndex, manualLabelEndIndex, fuzzyScoreFilename, labelScoreFilename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for combineData. ')

    parser.add_argument('--startIndex', type=int, required=True,
                        help='start index for the manually labeled data')
    parser.add_argument('--endIndex', type=int, required=True,
                        help='end index for the manually labeled data')
    parser.add_argument('--fuzzyScoreFile', type=str, required=True,
                        help='path to the fuzzy score file (the default is "fuzzyScores.txt"')
    parser.add_argument('--manualLabelFile', type=str, required=True,
                        help='path to the manually labeled file (the default is "1000annotate.csv")')
    parser.add_argument('--combined', action=argparse.BooleanOptionalAction, required=True,
                        help='select whether to combine manual label '
                             'and fuzzywuzzy label with both as 0 and 100 scores'
                             'need to use "--combined" or "--no-combined" in the arg')
    parser.add_argument('--outputFile', type=str, required=True,
                        help='path to the manually labeled file (the default is "groundTruth.txt")')
    args = parser.parse_args()
    combined = combineData(args.startIndex, args.endIndex, args.fuzzyScoreFile, args.manualLabelFile,
                           args.combined)
    outputFile = "groundTruth.txt"
    textfile = open(outputFile, "w")
    textfile.write("index,value\n")
    for element in combined:
        textfile.write(str(element[0]) + "," + str(element[1]) + "\n")
    textfile.close()

# current command line:
# python .\combineData.py --startIndex=0 --endIndex=1000 --fuzzyScoreFile="fuzzyScores.txt"
#   --manualLabelFile="1000annotate.csv" --combined --outputFile="groundTruth.txt"


