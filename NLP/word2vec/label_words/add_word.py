import numpy as np
import sys

from pathlib import Path


target_file = sys.argv[1];

loop_limit = 1;
if len(sys.argv) > 2:
    target_word = sys.argv[2];
else:
    loop_limit = -1;
    
index = 1;
while index != loop_limit:
    index += 1;
    already_exists = False;
    if(loop_limit == -1):
        target_word = input("target word -->");
    print("Adding ", target_word, " to ", target_file);

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
        continue;

    #####################
    ## Add the word to the file
    #####################
    if(file_exists):
        myfile = open(target_file, "a");
    else:
        myfile = open(target_file, "w+");
    myfile.write(target_word + "\n");
    myfile.close();
