from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# simple vs partial ratio
simpleRatio = fuzz.ratio("this is a test", "this is a test!")  # gives 97
# partialRatio = fuzz.partial_ratio("this is a test", "this is a test!")  # gives 100
partialRatio1 = fuzz.partial_ratio("This is a test", "this is a test!")  # gives 93 due to capital

# token sort ratio
r1 = fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")  # gives 91
tokenSortRatio = fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear") # 100
# token set ratio
r2 = fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear") # 84
tokenSetRatio = fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear") # 100

# process - extract
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
pExtract = process.extract("new york jets", choices, limit=2)
pExtractOne = process.extractOne("cowboys", choices)

# case insensitive
caseInsensitive = fuzz.token_set_ratio("I I am eating", "i am eating")
print(caseInsensitive)










