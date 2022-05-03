"""
This file is aimed to extract information from a csv file into txt.

input: wavo data (matching_data.csv)
output: a txt file with campaign name, artist name, and track name being extracted
     -- the format is:
<entity1> campaign name <entity2> <ASG_GROUPING_TITLE> trackName <ARTIST_DISPLAY_NAME> artistName

"""
import pandas as pd


# extract CSV file content to panda table
def extractCSV(filename="matching_data.csv"):
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["index", "CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME"]
    extractedColumns = df[columnNames]

    return extractedColumns, len(extractedColumns)


def extractInfo(targetFile, sourceFile, startIndex=0, endIndex=10):
    adjustEndIndex = extractCSV(sourceFile)[1]
    if endIndex <= adjustEndIndex:
        adjustEndIndex = endIndex

    file = open("{}".format(targetFile), "w")
    file.close()  # clear all the pre-existed content

    file = open("{}".format(targetFile), 'a', encoding='utf-8')  # append mode, encoding is necessary!

    extractedColumns = extractCSV(sourceFile)[0]
    for i in range(startIndex, adjustEndIndex):  # len(extractedColumns) is the max
        row = extractedColumns.iloc[i]  # convert each row to list of strings
        file.writelines("<entry1>  {}  <entry2> <artistName>  {}  <trackName>  {}\n".format(row[1], row[3], row[2]))
    file.close()


"""
Need to provide the source file and target file to output, and the start&end index of data to extract.
"""

target = "extract.txt"
source = "matching_data.csv"
start = 0
end = 1000

largestEndIndex = extractCSV(source)[1]  # extract all data with start = 0, end = largestEndIndex

extractInfo(target, source, start, end)
