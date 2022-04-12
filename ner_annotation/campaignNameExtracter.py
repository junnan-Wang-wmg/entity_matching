"""
The goal here is to extract unique campaign names from the wavo data (matching_data.csv).

input:
    Wavo data machint_data.csv

output:
    * The duplicate campaign names are removed.
    1. csv format - containing campaign_name, track_name, artist_name, index
    2. txt format - only campaign_name

"""

import pandas as pd


def extractCampaignName(filename, amount):
    df = pd.read_csv(r"{}".format(filename), index_col=0)
    df['index'] = range(0, len(df))
    columnNames = ["CAMPAIGN_NAME", "ASG_GROUPING_TITLE", "ARTIST_DISPLAY_NAME", "index"]
    df_campaignName = df[columnNames]
    uniqueCampaignName = df_campaignName.drop_duplicates(subset="CAMPAIGN_NAME")

    # output as csv and txt
    uniqueCampaignName.to_csv(r"campaign_name.csv", index= False)
    dataAmount = min(amount, len(uniqueCampaignName))
    uniqueCampaignName["CAMPAIGN_NAME"][:dataAmount].to_csv(r'campaignName.txt', index= False)


file = "matching_data.csv"
dataNumber = 400
extractCampaignName(file, dataNumber)

