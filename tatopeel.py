import sys
from os.path import exists
from typing import Dict, List, Any


# Stores the bases file to a dict
def read_bases(basefile: str):
    with open(basefile, newline='') as bfile:
        # Declares dictionary to return
        bases: Dict[Any, Any] = {}

        # Reads lines. At the time of writing, the python csv library causes undefined behavior.
        lines: List[str] = bfile.readlines()

        # Copies each id/base pair to a dictionary.
        for line in lines:
            # Splits the row into tabs: id, base.
            row = line.strip().split('	')

            # associates each sentence id (1st column) with its respective base (2nd column).
            bases[row[0]] = row[1]

        return bases


# Declares a function to obtain the id of what the specified sentence was originally translated from
def root_id(sentenceid, bases):
    if sentenceid not in bases or bases[sentenceid] == '\\N' or bases[sentenceid] == '0':
        # This is the root node. Pass the id up to whatever node requested the root.
        return sentenceid
    else:
        # Gets the root id of the parent node.
        return root_id(bases[sentenceid], bases)


# Generates parallel corpora from a dictionary of sentence bases, a list of lines from a Tatoeba sentences.csv,
# and two ISO 639-2 (3-letter) language codes, and writes them to the two specified files (or fake files for unit tests)
def convert(basemap: Dict[any, any], sentencelines: List[str], lang1: str, lang2: str, lang1file, lang2file):
    # Stores the sentences in the users' requested languages to a dictionary based on their root sentence bases
    sentenceforms = {}

    firstline: bool = True
    for line in sentencelines:
        # Splits the row into tabs: id, language, sentence.
        row = line.strip().split('	')

        # Checks if the language of the sentence (2nd column) is either of the parallel languages.
        if row[1] == lang1 or row[1] == lang2:
            # Gets the ID of the original sentence this was translated from.
            root = root_id(row[0], basemap)

            # Checks if we've seen a translation of this sentence before.
            if root in sentenceforms:
                # We've seen this sentence before. Checks to ensure it was in the other language.
                if sentenceforms[root][0] != row[1]:
                    # Unless it's the first line, add a line break to both files.
                    if firstline:
                        firstline = False
                    else:
                        lang1file.write('\n')
                        lang2file.write('\n')

                    # Checks to see which language the second instance of the sentence is in and writes to both files.
                    if row[1] == lang1:
                        lang1file.write(row[2])
                        lang2file.write(sentenceforms[root][1])
                    else:
                        lang2file.write(row[2])
                        lang1file.write(sentenceforms[root][1])
            else:
                # Puts this form of the sentence (language, sentence) in the dictionary for its base form
                # in case it exists in the other specified language.
                if root != '0' and root != '\\N':
                    sentenceforms[root] = [row[1], row[2]]


def main():
    # Proper syntax for the program. Used both in the help page and in argument errors.
    syntax = "tatopeel [sentencefile] [basefile] [lang1] [lang2]\n", \
             "example: tatopeel sentences.csv bases.csv eng spa\n", \
             "Please use extracted CSV files from tatoeba.org/downloads and ISO 639-2 (3-letter) language codes. "

    # Help page (tatopeel help). Also ensures the argument length is appropriate.
    if len(sys.argv) != 5:
        # Invalid arguments. Shows the user the appropriate arguments and exits the program.
        print(syntax)
        quit()

    # Stores arguments to readable variables
    sentencefile: str = sys.argv[1]
    basefile = sys.argv[2]
    lang1 = sys.argv[3]
    lang2 = sys.argv[4]

    # Reads the bases from the bases file into a dict
    bases = read_bases(basefile)

    if not exists(sentencefile):
        print("Invalid sentence file. You can find one on tatoeba.org/downloads.\n", "Proper syntax: " + syntax)

    if not exists(basefile):
        print("Invalid bases file. You can find one on tatoeba.org/downloads.\n", "Proper syntax: " + syntax)

    # Opens the sentences file and opens (or creates) the 2 parallel corpus files.
    with open(sentencefile, newline='', encoding="utf-8") as sfile, \
            open(lang1 + '.txt', 'w', encoding="utf-8") as lang1file, \
            open(lang2 + '.txt', 'w', encoding="utf-8") as lang2file:
        # Reads the lines of the sentence file into a list.
        lines: List[str] = sfile.readlines()

        # Creates parallel corpora from the bases/sentences and outputs them to the two files.
        convert(bases, lines, lang1, lang2, lang1file, lang2file)
