# tatopeel
Converts [Tatoeba](https://tatoeba.org/) base and sentences files into line delineated parallel corpora for use in deep learning machine translation applications.

# Installation
```sh
pip install git+https://github.com/akarisama/tatopeel.git
```

# Usage
```sh
tatopeel [sentences file] [bases file] [language code 1] [language code 2]
```
Tatopeel uses Tatoeba [files](https://tatoeba.org/downloads) for the sentences and bases and uses 3-letter [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) codes for the languages.
