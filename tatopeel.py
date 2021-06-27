import csv
import sys

# Ensures the argument length is appropriate. If not, shows the user the appropriate args and exits the program.
from typing import Dict, List, Any

if (len(sys.argv) != 5):
    print("tatopeel [sentencefile] [basefile] [lang1] [lang2]", "example: tatopeel sentences.csv bases.csv eng spa",
          "Please use extracted CSV files from tatoeba.org/downloads and ISO 639-2 language codes.", sep='\n')
    quit()

# Stores arguments to readable variables
sentencefile: str = sys.argv[1]
basefile = sys.argv[2]
lang1 = sys.argv[3]
lang2 = sys.argv[4]

# Stores the bases file to a dictionary
bases: Dict[Any, Any] = {}
with open(basefile, newline='') as bfile:
    # At the time of writing, the python csv library causes undefined behavior.
    lines = bfile.readlines()

    # Copies each base to the dictionary
    for row in lines:
        # Splits the row by tabs:
        srow = row.split('	')
        # bases[row['id']] = row['base']


# Declares a function to obtain the id of what the specified sentence was originally translated from
def root_id(sentenceid):
    if sentenceid not in bases or bases[sentenceid] == '\\N' or bases[sentenceid] == 0:
        # This is the root node. Pass the id up to whatever node requested the root.
        return sentenceid
    else:
        # Gets the root id of the parent node.
        return root_id(bases[sentenceid])


# Stores the sentences in the users' requested languages to a dictionary based on their root sentence bases
sentenceforms = {}
root: int = 0
with open(sentencefile, newline='', encoding="utf-8") as sfile, open(lang1 + '.txt', 'w',
                                                                     encoding="utf-8") as lang1file, open(
    lang2 + '.txt', 'w', encoding="utf-8") as lang2file:
    # Creates a csv reader for the sentences file
    reader = csv.DictReader(sfile, ["id", "lang", "data"], delimiter='	')

    # Runs through the file checking for sentences in the specified languages
    for row in reader:
        if row['lang'] == lang1 or row['lang'] == lang2:
            # Gets the ID of the original sentence this was translated from
            root = root_id(row['id'])

            # Checks if we've seen a translation of this sentence in the other specified language
            if root in sentenceforms:
                if sentenceforms[root][0] != row['lang']:
                    if row['lang'] == lang1:
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang2.
                        lang1file.write(row['data'] + '\n')
                        lang2file.write(sentenceforms[root][1] + '\n')
                    else:
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang1.
                        lang2file.write(row['data'] + '\n')
                        lang1file.write(sentenceforms[root][1] + '\n')
            else:
                # Puts this form of the sentence in the dictionary in case it exists in the other specified language.
                sentenceforms[root] = [row['lang'], row['data']]
