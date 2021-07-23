import sys
from typing import Dict, List, Any

# Ensures the argument length is appropriate.
if len(sys.argv) != 5:
    # Invalid arguments. Shows the user the appropriate args and exits the program.
    print("tatopeel [sentencefile] [basefile] [lang1] [lang2]", "example: tatopeel sentences.csv bases.csv eng spa",
          "Please use extracted CSV files from tatoeba.org/downloads and ISO 639-2 (3-letter) language codes.", sep='\n')
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
    # Reads lines.
    lines: List[str] = bfile.readlines()

    # Copies each id/base pair to a dictionary.
    for line in lines:
        # Splits the row into tabs: id, base.
        row = line.strip().split('	')

        # associates each sentence id (1st column) with its respective base (2nd column).
        bases[row[0]] = row[1]


# Declares a function to obtain the id of what the specified sentence was originally translated from
def root_id(sentenceid):
    if sentenceid not in bases or bases[sentenceid] == '\\N' or bases[sentenceid] == '0':
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
    # At the time of writing, the python csv library causes undefined behavior.
    # Reads lines
    lines: List[str] = sfile.readlines()

    # Runs through the file checking for sentences in the specified languages
    for line in lines:
        # Splits the row into tabs: id, language, sentence.
        row = line.strip().split('	')

        # Checks if the language of the sentence (2nd column) is either of the parallel languages.
        if row[1] == lang1 or row[1] == lang2:
            # Gets the ID of the original sentence this was translated from.
            root = root_id(row[0])

            # Checks if we've seen a translation of this sentence before.
            if root in sentenceforms:
                print(root)
                # We've seen this sentence before. Checks to ensure it was in the other language.
                if sentenceforms[root][0] != row[1]:
                    # Checks to see which language the second instance of the sentence is in.
                    if row[1] == lang1:
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang2.
                        lang1file.write(row[2] + '\n')
                        lang2file.write(sentenceforms[root][1] + '\n')
                    else:
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang1.
                        lang2file.write(row[2] + '\n')
                        lang1file.write(sentenceforms[root][1] + '\n')
            else:
                # Puts this form of the sentence (language, sentence) in the dictionary for its base form
                # in case it exists in the other specified language.
                if root != '0' and root != '\\N':
                    sentenceforms[root] = [row[1], row[2]]
