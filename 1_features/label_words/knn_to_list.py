import numpy as np
import sys
import add_word

import os

from pathlib import Path
##########################
## Takes a directory of input words to add to a list
###########################
'''
cd /var/www/git/NLP/SubjectWordClassification/1_features/label_words
python3 knn_to_list.py plant_words.txt KNN_related
'''
        
######################    
## Load user Input
######################
target_file = sys.argv[1];
source_directory = sys.argv[2];
if(target_file == "-h"):
    print("python3 add_word.py plant_words.txt");
    exit();

    
#######################
## Find all .txt files in source_directory
#######################
files = [];
for file in os.listdir(source_directory):
    if file.endswith(".txt"):
        filepath = (os.path.join(source_directory, file))
        files.append(filepath);
##print(files);        
print(len(files));

########################
## Load all words into memory, ensure each word only loaded once
########################
related_words = [];
seen_count = dict();
i = -1;
repeats = 0;
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
print ("repeats were : ", repeats);
print(seen_count[len(seen_count) - 50:]);

########################
## Add all words to target_file
########################
for this_tuple in seen_count:
    this_word = this_tuple[0];
    add_word.add_word(this_word, target_file);