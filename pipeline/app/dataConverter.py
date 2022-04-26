"""
dataConverter.py
Combine input campaign name, input artist name, and input track name to be a single input.

input file: wavo data (matching_data.csv)
output file: a txt file with campaign name, artist name, and track name being extracted


Example:
    input: (one row of the input file)
        campaign name: (partywithray Remix) BgBt - Minelli - Rampampam - P1 - R - 0062L00000VJP0VQAX [USA]
        artist name: Minelli
        track name: Rampampam

    output:
        (<entry1> campaign name <entry2> <artistName> artistName <trackName> trackName)

        "<entry1>  (partywithray Remix) BgBt - Minelli - Rampampam - P1 - R - 0062L00000VJP0VQAX [USA]
                 <entry2> <artistName>  Minelli  <trackName>  Rampampam"

"""
import pandas as pd
import argparse


# extract CSV file content to panda table
def extractCSV(filename="matching_data.csv"):
    """

    :param filename: input csv file path to evaluate. The file should contain the original data in csv. The data should
    contain campaign name, artist name,and track name. The dataset for this project is "matching_data.csv".
    :return: a panda dataframe contains the information from the original panda file. The number of the entries is also
    returned.
    """
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["index", "CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME"]
    extractedColumns = df[columnNames]

    return extractedColumns, len(extractedColumns)


def extractInfo(targetFile, sourceFile="matching_data.csv", startIndex=0, endIndex=10):
    """

    :param targetFile: output file path. Output the txt file with each line as the following format
                       <entry1> campaign name <entry2> <artistName> artistName <trackName> trackName
    :param sourceFile: input csv file path to evaluate. The file should contain the original data in csv. The data
    should contain campaign name, artist name,and track name. The dataset for this project is "matching_data.csv".
    :param startIndex: int, the starting index to extract from the source file.
    :param endIndex: int, the ending index to extract from the source file.
    :return:
    """
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
    print("The file is saved to {}".format(targetFile))
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    parser.add_argument('-t', '--target', type=str, required=True,
                        help='output file path (.txt)')
    parser.add_argument('-s', '--source', type=str, required=True,
                        help='input file path (.csv) with format as in "matching_data.csv"')
    parser.add_argument('--startIndex', type=int, required=True,
                        help='start index to analyze')
    parser.add_argument('--endIndex', type=int, required=True,
                        help='end index to analyze')
    args = parser.parse_args()
    extractInfo(args.target, args.source, args.startIndex, args.endIndex)
