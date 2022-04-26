"""
The goal here is to obtain the fuzzy wuzzy score for wavo data
in artistName vs campaignName and trackName vs campaign.

input:
    wavo data matching_data.csv
output:
    txt file containing index, artistScore, trackScore, and isMatching.
    *isMatching here is simply defined 1 with both 100 scores;
                                       0 with both 0 scores;
                                       0.5 otherwise
    The threshold is not adjusted in here.
"""

import pandas as pd
from fuzzywuzzy import fuzz
import re
import argparse


def fuzzyScore(filename="matching_data.csv", output="fuzzyScores.txt", amount=1000, isPreprocess=False):
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME", "index"]
    extractedColumns = df[columnNames]

    newTable1Title = {"index": [], "artistScore": [], "trackScore": []}
    newTable1 = pd.DataFrame(newTable1Title)

    # newTable2Title = {"index": [], "campaignName": [], "artist": [], "track": []}  # undetermined table
    # newTable2 = pd.DataFrame(newTable2Title)

    amount = min(amount, len(extractedColumns))

    for i in range(0, amount):  # change to len(extractedColumns) later
        row = extractedColumns.iloc[i]  # contains campaign name, track name, artist name
        campaignName = str(row[0]).lower()
        artistName = str(row[2]).lower()
        trackName = str(row[1]).lower()

        if isPreprocess:
            artistName = re.sub(r"\([^()]*\)", "", artistName)
            trackName = re.sub(r"\([^()]*\)", "", trackName)
        artistScore = fuzz.partial_ratio(campaignName, artistName)
        trackScore = fuzz.partial_ratio(campaignName, trackName)
        if artistName == trackName:
            artistScore, trackScore = 0, 0   # the artist name and track name should never be the same

        index = row[3]  # index in the matching_data.csv
        # if artistScore == 100 and trackScore == 100:
        #     isMatching = 1
        # elif artistScore == 0 and trackScore == 0:
        #     isMatching = 0
        # else:
        #     isMatching = 0.5    # setting 0.5 as uncertain label

        # pandaRow1 = pd.DataFrame({"index": [index], "artistScore": [artistScore],
        #                           "trackScore": [trackScore], "isMathing": [isMatching]})
        pandaRow1 = pd.DataFrame({"index": [index], "artistScore": [artistScore],
                                  "trackScore": [trackScore]})
        newTable1 = newTable1.append(pandaRow1)
        # if isMatching == 0.5:
        #     pandaRow2 = pd.DataFrame({"index": [index], "campaignName":
        #         [row[0]], "artist": [row[2]], "track": [row[1]]})
        #     newTable2 = newTable2.append(pandaRow2)

    # decreasedRatio = (len(newTable1) - len(newTable2)) / len(newTable1)
    # print("The decreased ratio is " + str(decreasedRatio) + ".")

    # output file
    newTable1.to_csv(r'{}'.format(output), index=False)
    # newTable2.to_csv(r'filteredData.txt', index=False)


# file = "matching_data.csv"
# # outputFile = "fuzzyScores_update.txt"
# numberData = 1000
# outputFile = "fuzzyScores_{}.txt".format(numberData)
# isPreprocessing = False
# fuzzyScore(file, outputFile, numberData, isPreprocessing)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    parser.add_argument('--file', type=str, required=True,
                        help='original file (matching_data.csv)')
    parser.add_argument('--output', type=str, required=True,
                        help='output file path (fuzzyScores.txt)')
    parser.add_argument('--dataCount', type=int, required=True,
                        help='number of data to analyze')
    # parser.add_argument('--manualLabelFile', type=str, required=True,
    #                     help='path to the manually labeled file (the default is "1000annotate.csv")')
    # parser.add_argument('-p', '--percentForArtistScore', nargs='+', required=True,
    #                     help='set a list of weight percentage for eval function')
    parser.add_argument('--preprocess', action=argparse.BooleanOptionalAction, required=False,
                        help='either choose to preprocess or not'
                             'use "--preprocess" or "--no-preprocess" in the arg')
    args = parser.parse_args()
    fuzzyScore(args.file, args.output, args.dataCount, args.preprocess)

