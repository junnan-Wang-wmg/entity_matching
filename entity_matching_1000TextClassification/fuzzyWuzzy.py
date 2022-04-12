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


def fuzzyScore(filename, output):
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME", "index"]
    extractedColumns = df[columnNames]

    newTable1Title = {"index": [], "artistScore": [], "trackScore": [], "isMathing": []}
    newTable1 = pd.DataFrame(newTable1Title)

    # newTable2Title = {"index": [], "campaignName": [], "artist": [], "track": []}  # undetermined table
    # newTable2 = pd.DataFrame(newTable2Title)

    for i in range(0, len(extractedColumns)):  # change to len(extractedColumns) later
        row = extractedColumns.iloc[i]  # contains campaign name, track name, artist name
        artistScore = fuzz.partial_ratio(str(row[0]), str(row[2]))
        trackScore = fuzz.partial_ratio(str(row[0]), str(row[1]))
        index = row[3]  # index in the matching_data.csv
        if artistScore == 100 and trackScore == 100:
            isMatching = 1
        elif artistScore == 0 and trackScore == 0:
            isMatching = 0
        else:
            isMatching = 0.5    # setting 0.5 as uncertain label

        pandaRow1 = pd.DataFrame({"index": [index], "artistScore": [artistScore],
                                  "trackScore": [trackScore], "isMathing": [isMatching]})
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


file = "matching_data.csv"
outputFile = "fuzzyScores.txt"
fuzzyScore(file, outputFile)
