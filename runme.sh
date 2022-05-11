# Setup annotation tool
doccano init
username=zhanlinwmg
password=test123
doccano createuser --username $username --password $password

# Process data
cd app
python dataConverter.py -t "../data/extract.txt"  -s "../data/matching_data.csv" --startIndex 0 --endIndex 1000
