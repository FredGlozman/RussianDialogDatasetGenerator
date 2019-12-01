# Russian Dialog Corpus
<b>The Russian Dialog Corpus is contained in the file titled <i>russians_rus.xml</i> at the root of this repository.<br>
Alternatively, the corpus can be viewed by navigating to the following webpage:</b>
  - https://github.com/FredGlozman/RussianDialogDatasetGenerator/blob/master/russians_rus.xml

# RussianDialogDatasetGenerator
A few Python scripts that crawl Russian forums, extract human conversations, and generate an XML corpus containing the acquired dialogs.

- University: McGill
- Course: COMP-551: Applied Machine Learning
- Instructor: Joelle Pineau
- Project 1: A multilingual dialogue dataset
- Due Date: September 27th 2017
- Team:     
  - Fred Glozman - fred.glozman@mail.mcgill.ca - 260635610 
  - Raihan Seraj  -raihan.seraj@mail.mcgill.ca - 260752605
  - Oruj Ahmadov - oruj.ahmadov@mail.mcgill.ca - 260523568

# Instructions

The following are the execution steps for generating a corpus containing the dialogs found on the following Russian forum: otvet.i.ua.
This repository also includes a script for generating a corpus for the following Russian forum: rususa.com

- Execute: 
  1. scrapy runspider RussianOtvetCrawler.py -o items.json
  2. python CorpusGenerator.py
  3. python CorpusAnalyzer.py
  
The file titled russians_rus.xml is the final Russian dialog corpus.
  
# About python3 branch
1. help-clean.ipynb
    * In the end of some lines of items.json, there might be a '\[' instead of a ',', which make json file broken. To help CorpusGenerator.py, we need to replace there ending with ',' in hand.
2. select_pair.ipynb
    * turn russians_rus.xml into a src and a tgt, which is the input files' format of [OpenNMT](https://github.com/OpenNMT/OpenNMT-py).