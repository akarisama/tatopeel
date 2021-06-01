import csv
import sys

# Ensures the argument length is appropriate. If not, shows the user the appropriate args and exits the program.
if(len(sys.argv) != 5):
    print("tatopeel [sentencefile] [basefile] [lang1] [lang2]", "example: tatopeel sentences.csv bases.csv eng spa", "Please use extracted CSV files from tatoeba.org/downloads and ISO 639-2 language codes.", sep='\n')
    quit()

# Stores arguments to readable variables
sentencefile = sys.argv[1]
basefile = sys.argv[2]
lang1 = sys.argv[3]
lang2 = sys.argv[4]

# Stores the bases file to a dictionary
bases = {}
with open(basefile, newline='') as bfile:
    # Creates a csv reader for the sentence base file
    reader = csv.DictReader(bfile, {"id", "base"}, delimiter='	')

    # Copies each base to the dictionary
    for row in reader:
        bases[row['id']] = row['base']

# Declares a function to obtain the id of what the specified sentence was originally translated from
def RootId(id):
    if(id not in bases or id == '\\N' or id == 0):
        # This is the root node. Pass the id up to whatever node requested the root.
        return id
    else:
        # Gets the root id of the parent node.
        return RootId(bases[id])

# Stores the sentences in the users' requested languages to a dictionary based on their root sentence bases
sentenceforms = {}
rootid = 0
with open(sentencefile, newline='', encoding="utf-8") as sfile, open(lang1 + '.txt', 'w', encoding="utf-8") as lang1file, open(lang2 + '.txt', 'w', encoding="utf-8") as lang2file:
    # Creates a csv reader for the sentences file
    reader = csv.DictReader(sfile, ["id", "lang", "data"], delimiter='	')
    
    # Runs through the file checking for sentences in the specified languages
    for row in reader:
        if(row['lang'] == lang1 or row['lang'] == lang2):
            # Gets the ID of the original sentence this was translated from
            rootid = RootId(row['id'])

            # Checks if we've seen a translation of this sentence in the other specified language
            if(rootid in sentenceforms):
                if(sentenceforms[rootid][0] != row['lang']):                  
                    if(row['lang'] == lang1):
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang2.
                        lang1file.write(row['data']+'\n')
                        lang2file.write(sentenceforms[rootid][1]+'\n')
                    else:
                        # Saves the sentence and saved sentence to file since we've already seen this sentence in lang1.
                        lang2file.write(row['data']+'\n')
                        lang1file.write(sentenceforms[rootid][1]+'\n')
            else:
                # Puts this form of the sentence in the dictionary in case it exists in the other specified language.
                sentenceforms[rootid] = [row['lang'], row['data']]