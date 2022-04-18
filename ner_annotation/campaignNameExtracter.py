"""
The goal here is to extract unique campaign names from the wavo data (matching_data.csv).

input:
    Wavo data machint_data.csv

output:
    * The duplicate campaign names are removed.
    1. csv format - containing campaign_name, track_name, artist_name, index
    2. txt format - only campaign_name

"""

import argparse
import pandas as pd

def extractCampaignName(filename, start, end, out_path):
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME", "index"]
    df_campaignName = df[columnNames]
    uniqueCampaignName = df_campaignName.drop_duplicates(subset="CAMPAIGN_NAME")

    # output as csv and txt
    output_csv = out_path + '.csv'
    output_txt = out_path + '.txt'
    uniqueCampaignName.to_csv(output_csv, index= False)
    if start > len(uniqueCampaignName):
        print('Out of annotation range')
        return
    end = min(end, len(uniqueCampaignName))
    uniqueCampaignName["CAMPAIGN_NAME"][start:end].to_csv(output_txt, index= False)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='parameters for extract campaign names. ')

    parser.add_argument('--file_path', type=str, required=True,
                        help='path to the data.')
    parser.add_argument('--start', type=int, required=True, help='start number to annotate')
    parser.add_argument('--end', type=int, required=True, help='end number to annotate')
    parser.add_argument('--out_path', type=str, required=True, help='path to output file')
    args = parser.parse_args()
    extractCampaignName(args.file_path, args.start, args.end, args.out_path)

# file = "matching_data.csv"
# dataNumber = 400
# extractCampaignName(file, dataNumber)

# current run method:
# python .\campaignNameExtracter.py --file_path="matching_data.csv" --start=0 --end=400 --out_path="campaignName400"
