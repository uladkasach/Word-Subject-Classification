###################
## Sort words in labels by words who have enough frequency in vector embedding data set to be accurate and those who do not 
###################

import sys;
import csv # to load data
import collections # to get most common words
from pathlib import Path;

######################################
## Defaults
######################################
TRUE_LABEL_SOURCE = '../label_words/plant_words.txt';
FALSE_LABEL_SOURCE = '../label_words/nonplant_words.txt';

######################################
## Read SysArgs
######################################
min_word_frequency_threshold = int(sys.argv[1]);
delta_mod = str(sys.argv[2]);
if(len(sys.argv) > 3):
    delta_mod_save = "_" + str(sys.argv[3]); 
else:
    delta_mod_save = "";

########################################
## offer help for -h
#######################################
if(delta_mod == "-h"):
    print("example : python3 frequency_parse.py 10 inputs/5.6m_basic_freq_table.csv [filenamemod = none]");
    exit();
    
    
#####################################
## Generate dynamic file names
#####################################
file_path_to_read_frequencies_from = delta_mod;
true_labels_save_path = 'results/frequent_plant_words'+delta_mod_save+'.txt';
true_unfreq_labels_save_path = 'results/unfrequent_plant_words'+delta_mod_save+'.txt';
false_labels_save_path = 'results/frequent_nonplant_words'+delta_mod_save+'.txt';
false_unfreq_labels_save_path = 'results/unfrequent_nonplant_words'+delta_mod_save+'.txt';
print(true_labels_save_path);
print(false_labels_save_path);


#######################################
## Verify that user wants to overwrite files, if files with the mod names already exist
#######################################
my_file = Path(true_labels_save_path);
if my_file.is_file():
    print("A file name with the specified dynamic arguments you've specified (e.g., ", true_labels_save_path, ") already exists. Are you sure you want to overwrite it?");
    result = input("YES/no: ").lower();
    print (result);
    if(result == "y" or result == "yes"):
        print("Ok! Overwriting");
        #continue
    else:
        exit();
        
        
#######################################
## Load Frequent Words
#######################################
print("Loading Frequent Words...");
frequent_words = [];
file_name = file_path_to_read_frequencies_from;
print(" -- Source filename " + file_name);
f = open(file_name, 'r');
for line in f.readlines():
    parts = line.rstrip().split(",");
    #print(parts);
    word = parts[0];
    freq = int(parts[1]);
    if(freq >= min_word_frequency_threshold):
        frequent_words.append(word);
f.close();
print(" -- Words frequent enough in total: ", len(frequent_words), '\n');

        
        
def frequency_parse_labels(frequent_words, path_to_analyze):
    frequent_labels = [];
    unfrequent_labels = [];
    file_name = path_to_analyze;
    print(" -- Source filename " + file_name);
    f = open(file_name, 'r');
    for line in f.readlines():
        parts = line.split();
        word = parts[0];
        if(word in frequent_words):
            frequent_labels.append(word);
        else:
            unfrequent_labels.append(word);
    f.close();
    return frequent_labels, unfrequent_labels;

def list_save(the_path, the_list):
    print(" -- Writing to filename " + the_path);
    f = open(the_path, 'w+')
    for this_word in the_list:
        f.write(this_word+'\n');  # python will convert \n to os.linesep
    f.close()  
##########################################
## Parse and Save Labels
##########################################
print("Parsing Positive Labels...");
frequent_labels, unfrequent_labels = frequency_parse_labels(frequent_words, TRUE_LABEL_SOURCE);
list_save(true_labels_save_path, frequent_labels);
list_save(true_unfreq_labels_save_path, unfrequent_labels);
print(frequent_labels[0:10], "\n", unfrequent_labels[0:10]);

print("Parsing Negative Labels...");
frequent_labels, unfrequent_labels = frequency_parse_labels(frequent_words, FALSE_LABEL_SOURCE);
list_save(false_labels_save_path, frequent_labels);
list_save(false_unfreq_labels_save_path, unfrequent_labels);
print(frequent_labels[0:10], "\n", unfrequent_labels[0:10]);

print("All Done");