import numpy as np
import sys
import add_word

import os

from pathlib import Path
##########################
## Takes a directory of input words to add to a list
###########################
'''
cd /var/www/git/NLP/Word-Subject-Classification/1_features/label_words
python3 merge_words.py google_plant_words.txt new_words.txt
'''
        
######################    
## Load user Input
######################
remove = False;
target_file = sys.argv[1];
source_file = sys.argv[2];
if(len(sys.argv) > 3):
    if(sys.argv[3] == "remove"):
        remove = True;
    else:
        print("Argument 3 does not make sense. Error.");
        exit();
########################
## Load all words into memory, ensure each word only loaded once
########################
related_words = [];
seen_count = dict();
i = -1;
repeats = 0;
files = [source_file];
for a_file in files:
    if Path(a_file).is_file():
        f = open(a_file, 'r');
        for line in f.readlines():
            ## Open it and for each word add it to the list if it is not already in list
            i += 1;
            parts = line.split();
            this_word = parts[0];
            if this_word not in related_words:
                related_words.append(this_word);
                seen_count[this_word] = 1;
            else:
                repeats += 1;
                seen_count[this_word] += 1;
            if i % 50 == 0:
                print(" Reading word ", i);
        f.close();
seen_count = sorted(seen_count.items(), key=lambda x: x[1], reverse = True);
##print(related_words[0:5]);
##print(len(related_words));
print(seen_count[len(seen_count) - 50:]);

########################
## Add all words to target_file
########################
for index, this_tuple in enumerate(seen_count):
    this_word = this_tuple[0];
    if(remove == False): add_word.add_word(this_word, target_file);
    if(remove == True):  add_word.remove_word(this_word, target_file);
    
    
    
    