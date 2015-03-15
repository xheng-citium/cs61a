from collections import OrderedDict
import re, os
from data import DATA_PATH

care_emotion_symbol = False # True or False (default)
run_spell_corrector = False # True or False (default)
find_state_by       = "by_statecenter" # "by_statecenter" (default), "by_stateborders"

class CONSTANTS:
    def __init__(self, care_emotion_symbol, run_spell_corrector, find_state_by):
        self._find_state_by = find_state_by
        if self._find_state_by != "by_stateborders":
            self._find_state_by = "by_statecenter" # Insert default value

        self._care_emotion_symbol = care_emotion_symbol 
        if self._care_emotion_symbol is not True: # in case user types in run_spell_corrector = "1"
            self._care_emotion_symbol = False 
    
        self._run_spell_corrector = run_spell_corrector
        if self._run_spell_corrector is not True:
            self._care_emotion_symbol
    
    def print_all(self):
        print("\nInside constants:")
        print("find_state_by       =",self.find_state_by)
        print("care_emotion_symbol =",self.care_emotion_symbol)
        print("run_spell_corrector =",self.run_spell_corrector)
    
    # Follwing is a trick to mimic Python constants. For example, you can use constants.find_state_by, but calling constants.find_state_by = "xyz" will raise AttibuteError
    @property
    def find_state_by(self):
        return self._find_state_by
    @property
    def care_emotion_symbol(self):
        return self._care_emotion_symbol
    @property
    def run_spell_corrector(self):
        return self._run_spell_corrector

constants = CONSTANTS(care_emotion_symbol, run_spell_corrector, find_state_by)

##################################################
# a dictionary of emotion symbols and their values
emotion_values = OrderedDict()
emotion_values[":)"]  =  0.6 
emotion_values[":-)"] =  0.7 
emotion_values[":("]  = -0.5
emotion_values[":-("] = -0.6

#############################################
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

