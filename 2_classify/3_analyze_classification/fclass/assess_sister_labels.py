import numpy as np;
import pandas as pd;
import sys;
import matplotlib.pyplot as plt;
from tabulate import tabulate;
import subprocess;

'''
cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/fclass; python3 assess_sister_labels.py
'''

################################
## For each word in a false positive list check whether it is in one of the sister class lists. If so, increment the counter for the relative word
################################
start_index = 0;
removal = False;
if(len(sys.argv) > 1):
    start_index = int(sys.argv[1]);
if(len(sys.argv) > 2 and sys.argv[2] == "remove"):
    removal = True;
this_file = "TOP_FN_R4.txt"; ## 1606



#####################################
## Load sister classes
#####################################
sister_classes = dict({
        "plants" : dict({
                "counter" : 0,
                "file_title" : "google_plant_words.txt",
                "data" : [],
                }),
        "food" : dict({
                "counter" : 0,
                "file_title" : "food_words.txt",
                "data" : [],
                }),
        "gardening" : dict({
                "counter" : 0,
                "file_title" : "gardening_words.txt",
                "data" : [],
                }),
        "ecosystems" : dict({
                "counter" : 0,
                "file_title" : "ecosystem_words.txt",
                "data" : [],
                }),
        });
for key, value in sister_classes.items():
    file_title = value["file_title"];
    words = [];
    
    target_file = "/var/www/git/NLP/Word-Subject-Classification/1_features/label_words/" + file_title; 
    f = open(target_file, 'r');
    i = -1;
    for index, line in enumerate(f.readlines()):
        i += 1;
        parts = line.split();
        this_word = parts[0];
        words.append(this_word);
    f.close();
    
    sister_classes[key]["data"] = words;
    #print(words[0:10]);
    #print(len(words));
    

#########################################
## Evaluate words
#########################################
with open(this_file, 'r') as fp:
    source_lines = fp.readlines();
    total_lines = len(source_lines);
    for index, line in enumerate(source_lines):
        full_index = index;
        if(index < start_index): continue;
        parts = line.rstrip().split(" ");
        if(parts[0] == ""): continue;
        if(len(parts) < 2): continue;
        the_word = parts[1]; 

        ###################################################
        ## Check if word is already labeled as a sister class word
        ###################################################
        already_labeled = False;
        '''
        for index, sister_class_file in enumerate(sister_class_files):
            base_path = "/var/www/git/NLP/Word-Subject-Classification/1_features/label_words/";
            command = "cd " + base_path + " && python3 is_word_present.py " + sister_class_file + " "+the_word;
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
            if(result.decode('ascii') == "true\n"):
                print("Word (" + the_word + ") was already found in " + sister_class_file);
                already_labeled = True;
                sister_class_counter[index] += 1;
                break;
        '''
        for key, value in sister_classes.items():
            these_words = value["data"];
            if the_word in these_words: 
                sister_classes[key]["counter"] += 1;
                break;
        
        if(full_index % 200 == 0):
            print(full_index, "/", total_lines);


            
##########################################
## Output results
##########################################
for key, value in sister_classes.items():
    this_file = value["file_title"];
    this_count = value["counter"];
    print(this_file, " : ", this_count); 

