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

this_file = "FP_R1.txt";
with open(this_file, 'r') as fp:
    source_lines = fp.readlines();
    for index, line in enumerate(source_lines):
        if(index < start_index): continue;
        parts = line.rstrip().split(" ");
        if(parts[0] == ""): continue;
            
        print("now checking " + str(index) + " -> " + line.rstrip());
        response = input("You like? ");
        
        the_word = parts[1]; 
        the_path = "/var/www/git/NLP/Word-Subject-Classification/1_features/label_words/";
        if(removal == False):
            if(response in ["Y", "y"]):
                command = "cd " + the_path + " && python3 add_word.py new_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);
            if(response in ["F", "f"]):
                command = "cd " + the_path + " && python3 add_word.py food_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);
                
        if(removal == True):
            if(response in ["R", "r"]):
                command = "cd " + the_path + " && python3 add_word.py remove_words.txt "+the_word;
                #print(command);
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read();
                print(result);