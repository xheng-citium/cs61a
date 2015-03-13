from collections import OrderedDict
import re, os
from data import DATA_PATH

CARE_EMOTION_SYMBOL = False # True or False (default)
RUN_SPELL_CORRECTOR = False # True or False (default)
FIND_STATE          = "by_statecenter" # "by_statecenter" (default), "by_stateborders"

# a dictionary of emotion symbols and their values
EMOTION_VALUES = OrderedDict()
EMOTION_VALUES[":)"]  =  0.6 
EMOTION_VALUES[":-)"] =  0.7 
EMOTION_VALUES[":("]  = -0.5
EMOTION_VALUES[":-("] = -0.6

def count_all_words( dictionary_file = DATA_PATH + "big_dictionary.txt"):
    """Count all words in the dictionary file
    Returns a dict data:{ word: # of counts... } """
    assert os.path.isfile( dictionary_file), dictionary_file + " is not found"
    f = open(dictionary_file, "r")
    all_words = []
    for line in f: 
        all_words += re.findall('[a-z]+', line.lower()) 
    f.close()

    model = {}
    for w in all_words:
        if w in model: model[w] += 1
        else: model[w] = 1
    return model
NWORDS = count_all_words() 

