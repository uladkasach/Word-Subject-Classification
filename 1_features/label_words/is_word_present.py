import numpy as np
import sys

from pathlib import Path
'''
cd /var/www/git/NLP/Word-Subject-Classification/1_features/label_words; 
python3 add_word.py new_words.txt 
'''

def check_for_presence(target_word, target_file):
    already_exists = False;
    ######################
    ## Ensure that word does not already exist in the list
    ######################
    ## 1) check if file exists
    file_exists = True;
    my_file = Path(target_file);
    if my_file.is_file():
        ## 2) run through each line and check if word is there
        f = open(target_file, 'r');
        i = -1;
        for line in f.readlines():
            i += 1;
            parts = line.split();
            this_word = parts[0];

            if(this_word == target_word):
                already_exists = True;
                break;
        f.close();
    else:
        file_exists = False;

    if(already_exists):
        print("true");
    else:
        print("false");

    
if __name__ == "__main__":
    
    target_file = sys.argv[1];
    test_word = sys.argv[2];

    if(target_file == "-h"):
        print("python3 add_word.py plant_words.txt");
        exit();

    check_for_presence(test_word, target_file);