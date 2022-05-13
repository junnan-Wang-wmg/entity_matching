"""
fuzzyWuzzy.py
Obtain fuzzy scores for each entry of campaign name, artist name, and track name. There will be two scores:
1. artist score: campaign name vs artist name
2. track score: campaign name vs track name

Example:
    input: (one row of the input file)
        campaign name: (partywithray Remix) BgBt - Minelli - Rampampam - P1 - R - 0062L00000VJP0VQAX [USA]
        artist name: Minelli
        track name: Rampampam
    output:
        artistScore: 100
        trackScore: 100

"""

import pandas as pd
from fuzzywuzzy import fuzz
import re
import argparse


def fuzzyScore(filename="matching_data.csv", output="fuzzyScores.txt", startIndex=0, endIndex=1000, isPreprocess=False):
    """

    :param filename: input csv file path to evaluate. The file should contain the original data in csv. The data should
    contain campaign name, artist name,and track name. The dataset for this project is "matching_data.csv".
    :param output: output txt file path. Each entry is with the following format:
                    index, artistScore, trackScore
    :param startIndex: int, the starting index to extract from the source file.
    :param endIndex: int, the ending index to extract from the source file.
    :param isPreprocess: boolean, determine whether to perform preprocessing before accessing the fuzzy score.
                        The current preprocessing contains:
                         1. the removal of brackets in the input artist and track names.
    :return: a txt file. Each entry is with the following format:
                index, artistScore, trackScore
    """
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME", "index"]
    extractedColumns = df[columnNames]

    # newTable1Title = {"index": [], "artistScore": [], "trackScore": []}
    newTable1Title = {"index": [], "artistScore": [], "trackScore": [], "entry": []}
    newTable1 = pd.DataFrame(newTable1Title)

    endIndex = min(endIndex, len(extractedColumns))

    for i in range(startIndex, endIndex):  # change to len(extractedColumns) later
        row = extractedColumns.iloc[i]  # contains campaign name, track name, artist name
        campaignName = str(row[0]).lower()
        artistName = str(row[2]).lower()
        trackName = str(row[1]).lower()

        if isPreprocess:
            artistName = re.sub(r"\([^()]*\)", "", artistName)
            artistName = re.sub(r"\[[^()]*\]", "", artistName)
            trackName = re.sub(r"\([^()]*\)", "", trackName)  # remove content in ()
            trackName = re.sub(r"\[[^()]*\]", "", trackName)  # remove content in []
        artistScore = fuzz.partial_ratio(campaignName, artistName)
        trackScore = fuzz.partial_ratio(campaignName, trackName)
        if artistName == trackName:
            artistScore, trackScore = 0, 0   # the artist name and track name should never be the same

        index = row[3]  # index in the matching_data.csv

        # pandaRow1 = pd.DataFrame({"index": [index], "artistScore": [artistScore],
        #                           "trackScore": [trackScore]})
        pandaRow1 = pd.DataFrame({"index": [index], "artistScore": [artistScore],
                                  "trackScore": [trackScore], "entry": [campaignName]})
        # newTable1 = newTable1.append(pandaRow1)
        newTable1 = pd.concat([newTable1, pandaRow1])

    # output file
    outputFilePath = output.replace(".txt", "_") + str(startIndex) + "-" + str(endIndex) + ".txt"
    newTable1.to_csv(r'{}'.format(outputFilePath), index=False)
    print("The output is in {}.".format(outputFilePath))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    parser.add_argument('--file', type=str, required=True,
                        help='original file (matching_data.csv)')
    parser.add_argument('--output', type=str, required=True,
                        help='output file path (fuzzyScores.txt)')
    parser.add_argument('--startIndex', type=int, required=True,
                        help='number of data to analyze')
    parser.add_argument('--endIndex', type=int, required=True,
                        help='number of data to analyze')
    parser.add_argument('--preprocess',action='store_true', required=False,
                        help='either choose to preprocess or not'
                             'use "--preprocess" or "--no-preprocess" in the arg')
    args = parser.parse_args()
    fuzzyScore(args.file, args.output, args.startIndex, args.endIndex, args.preprocess)

