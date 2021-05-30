import csv
import sys

# Ensures the argument length is appropriate. If not, shows the user the appropriate args and exits the program.
if(len(sys.argv) != 4):
    print("tatopeel.py [sentences.csv] [sentences_base.csv] [lang1] [lang2]")
    quit()

# Checks that the languages are appropriate

# Reads the files to the dictionaries

# Opens the sentences csv
with open(sys.argv[1], newLine='') as csvfile:
    # Creates a csv reader 
    reader = csv.DictReader(csvfile, {"id", "lang", "data"})

    for row in reader:
        if(row['lang'] == "eng" or row['lang'] == "spa"):
            






# Iterates over the dictionary to the new file.