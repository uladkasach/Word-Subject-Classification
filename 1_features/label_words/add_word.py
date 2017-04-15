import numpy as np
import sys

from pathlib import Path
'''
cd /var/www/git/NLP/Word-Subject-Classification/1_features/label_words
python3 add_word.py plant_words.txt 
'''

def add_word(target_word, target_file):
    print("Adding ", target_word, " to ", target_file);
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
        print(target_word, " already exists in ", target_file);
        return;
    
    #####################
    ## Add the word to the file
    #####################
    if(file_exists):
        myfile = open(target_file, "a");
    else:
        myfile = open(target_file, "w+");
    myfile.write(target_word + "\n");
    myfile.close();

    
def remove_word(target_word, target_file):
    target_word = target_word.strip();
    print("Removing `", target_word, "` from ", target_file);
    f = open(target_file,"r+")
    d = f.readlines()
    f.seek(0)
    skipped_it = False;
    for i in d:
        if i.rstrip() != target_word:
            f.write(i)
        else:
            skipped_it = True;
    f.truncate()
    f.close()
    if(skipped_it):
        print("Successfuly removed.");
    else:
        print("Word did not exist in set.");
    
def return_word_count():
    with open(target_file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
if __name__ == "__main__":
    
    target_file = sys.argv[1];

    if(target_file == "-h"):
        print("python3 add_word.py plant_words.txt");
        exit();

    loop_limit = 1;
    if len(sys.argv) > 2:
        target_word = sys.argv[2];
    else:
        loop_limit = -1;

    
    index = 1;
    while index != loop_limit:
        index += 1;
        if(loop_limit == -1):
            target_word = input("target word -->").rstrip();##.lower()
        if(str(target_word) == str("count")):
            print (return_word_count());
            continue;
        elif(str(target_word)[0:2] == "-x"):
            remove_word(str(target_word)[2:], target_file);
            continue;
        else:
            add_word(str(target_word), target_file);
    
        
        