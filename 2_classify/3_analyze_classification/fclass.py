######################
## Script generates statistics on which words were misclassified the most - choose either FP or FN
######################
##############################
## Grabs either FP or FN from analysis results for all results. Sorts in order of descending frequency. Outputs to list w/ file name.
##############################

'''
cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/; python3 fclass.py TOP_FN_R1 FN Ar1_enum_488_r0_result.csv
'''

from os import listdir;
import os;
from os.path import isfile, join
import numpy as np;
import pandas as pd;
import sys;
import matplotlib.pyplot as plt
from tabulate import tabulate

#######################################
## User Inputs
#######################################
RESULTS_ROOT = "results/test_1_all/";
DELTA_MOD = sys.argv[1];
TYPE = sys.argv[2].upper();
if(TYPE not in ["TP", "FP"]): 
    print("Type selected not valid");
specific_file = None;
if(len(sys.argv) > 3):
    specific_file = sys.argv[3];

if(specific_file is None):
    print('Detecting all files....');
    #######################################
    ## Detect all results in results directory
    #######################################
    results_root = RESULTS_ROOT;
    result_files = [f for f in listdir(results_root) if isfile(join(results_root, f))]
    #result_files.remove('.gitignore');
    result_files_old = result_files;
    result_files = [s for s in result_files_old if s.endswith(".csv")]
    print("Found ", len(result_files), " files.");
    #print(len(result_files));
    #exit();
else:
    result_files = [specific_file];


print('Loading all relevant results...');
#######################################
## Load All Results
#######################################
words_found = dict();
for this_file in result_files:
    ####
    ## For each file, find the relevant FP or FN
    ####
    print(this_file);
    relevant_found = False;
    with open(RESULTS_ROOT + this_file, 'r') as fp:
        source_lines = fp.readlines();
        for line in source_lines:
            parts = line.rstrip().split(" ");
            if(parts[0] == ""): continue;
            if(relevant_found == False):
                if(len(parts) > 2 and parts[1] == TYPE): 
                    relevant_found = True;
                continue; 
            if(relevant_found == True):
                if(len(parts) > 1): 
                    break; # found the next section, this section is done.
            #########################
            ## If we are here, then we are in on data row
            #########################
            parts = parts[0].split(",");
            the_word = parts[2];
            if(the_word not in words_found):
                words_found[the_word] = 0;
            words_found[the_word] += 1;
    
##########################################
## Record in Descending order
##########################################
print("Writing to file....");
directory = "fclass";
if not os.path.exists(directory):
    os.makedirs(directory)
output_file = open("fclass/"+DELTA_MOD+".txt", "w+"); 
for i, w in enumerate(sorted(words_found, key=words_found.get, reverse=True)):
    output_file.write(str(words_found[w]) + " " + w + "\n");
    if(i % 500 == 0): print("at word ", i);
    
