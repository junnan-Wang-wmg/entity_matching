file_path="matching_data.csv"
start=0
end=1000
out_path="campaignName400_n"
python ner_annotation/campaignNameExtracter.py --file_path=$file_path --start=$start --end=$end --out_path=$out_path