import numpy as np;
import pandas as pd;
import sys;
import matplotlib.pyplot as plt;
from tabulate import tabulate;
import subprocess;

'''
cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/fclass; python3 add_to_list.py 
'''

start_index = 0;
removal = False;
if(len(sys.argv) > 1):
    start_index = int(sys.argv[1]);
if(len(sys.argv) > 2 and sys.argv[2] == "remove"):
    removal = True;

this_file = "TOP_FP_R4.txt"; ## 1606
with open(this_file, 'r') as fp:
    source_lines = fp.readlines();
    for index, line in enumerate(source_lines):
        if(index < start_index): continue;
        parts = line.rstrip().split(" ");
        if(parts[0] == ""): continue;
        the_word = parts[1]; 
            
            
        
        ###################################################
        ## Check if word is already labeled as a sister class word
        ###################################################
        if(False):
            the_path = "/var/www/git/NLP/Word-Subject-Classification/1_features/label_words/";
            sister_class_files = ["food_words.txt", "gardening_words.txt", "ecosystem_words.txt"];
            target_class_files = ["new_words_4.txt", "remove_words_4.txt"];
            all_relevent_class_files = [];
            #all_relevent_class_files.extend(sister_class_files)
            all_relevent_class_files.extend(target_class_files);
            already_labeled = False;
            for sister_class_file in all_relevent_class_files:
                command = "cd " + the_path + " && python3 is_word_present.py " + sister_class_file + " "+the_word;
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                if(result.decode('ascii') == "true\n"):
                    print("Word (" + the_word + ") was already found in " + sister_class_file);
                    already_labeled = True;
                    break;
            if(already_labeled == True):
                continue;
            
            
        ###################################################
        ## Check if word is already labeled as a sister class word, remove it from TP since we are looking at FN
        ###################################################
        force_removal = False;
        if(False):
            if(removal == True):
                already_labeled = False;
                sister_class_files = ["food_words.txt", "gardening_words.txt", "ecosystem_words.txt"];
                for sister_class_file in sister_class_files:
                    command = "cd " + the_path + " && python3 is_word_present.py " + sister_class_file + " "+the_word;
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                    if(result.decode('ascii') == "true\n"):
                        print("Word (" + the_word + ") was already found in " + sister_class_file);
                        already_labeled = True;
                        break;
                if(already_labeled == True):
                    force_removal = True;
                    response = "r";
            
            
            
        ###################################################
        ## If not already classified as sister class, let user choose label if desired
        ###################################################
        print("now checking " + str(index) + " -> " + line.rstrip());
        while True: ## Loop enables user to pick multiple files to add to
            ##########
            ## Ask
            ##########
            if(force_removal != True):
                response = input("You like? ");

            if(response.rstrip() == ""): break;

            ##########
            ## Do
            ##########
            the_path = "/var/www/git/NLP/Word-Subject-Classification/1_features/label_words/";
            if(removal == False):
                if(response in ["Y", "y", "t"]):
                    command = "cd " + the_path + " && python3 add_word.py new_words_4.txt "+the_word;
                    #print(command);
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                    print(result);

            sister_label = False;
            if(response in ["F", "f"]):
                command = "cd " + the_path + " && python3 add_word.py food_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);
                sister_label = True;
            if(response in ["G", "g"]):
                command = "cd " + the_path + " && python3 add_word.py gardening_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);
                sister_label = True;
            if(response in ["e"]):
                command = "cd " + the_path + " && python3 add_word.py ecosystem_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);
                sister_label = True;

            if(removal == True):
                if(response in ["R", "r"] or sister_label == True):
                    command = "cd " + the_path + " && python3 add_word.py remove_words_4.txt "+the_word;
                    #print(command);
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                    print(result);