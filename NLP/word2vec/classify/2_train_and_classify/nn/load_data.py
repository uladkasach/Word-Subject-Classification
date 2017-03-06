###############
## Import Libraries
###############
import tensorflow as tf
import sys
import numpy as np;
import random;
import datetime;

##########################################################################
## Return Regular Batch
##########################################################################
def return_regular_batch(data_source_path, batch_size):
    global data_source_lines;
    global data_source_lines_index;
    
    
    ########################
    ## Initialize global variables if they do not exist
    ########################
    if 'data_source_lines' not in globals():
        data_source_lines = {
            "train" : None,
            "test" : None,
        }   
        data_source_lines_index = {
            "train" : 0,
            "test" : 0,
        }

    ######################
    ## Detect data source type
    ######################
    data_source_path = data_source_path[0];
    if ("test.csv" in data_source_path):
        this_source_type = "test";
    elif ("train.csv" in data_source_path):
        this_source_type = "train";
    else:
        print(" Data Source path is not a test or train type. Error.");
        exit();

        
    #######################
    ## Load this source data into memory if it is not already there
    #######################
    if(data_source_lines[this_source_type] is None):
        print("Loading ", this_source_type, " data");
        with open(data_source_path) as fp:
            source_lines = fp.readlines();
        random.shuffle(source_lines);
        data_source_lines[this_source_type] = source_lines;
    else:
        source_lines = data_source_lines[this_source_type];
        
    
    
    ## Load settings
    one_hot_depth = 2;
    
    
    if(batch_size > 0):
        batch_data_length = batch_size;
    else:
        batch_data_length = len(source_lines);
    keys_list = []; ## only supports one key per row atm
    y_data = np.zeros([batch_data_length, one_hot_depth], 'float');
    feature_data = None; #numpy.zeros([batch_size, len(feature_index)], 'float');
    ## Grab and parse data
    
    i = data_source_lines_index[this_source_type];
    while (len(keys_list) != batch_data_length):
        i += 1;
        if(i >= len(source_lines) - 1):
            random.shuffle(source_lines);
            data_source_lines[this_source_type] = source_lines;
            i = 0;
            print("Shuffling source_lines!");
            
        line = source_lines[i];
        
        parts = line.rstrip().split(",");
        if(parts[0] == 'label'):
            continue; # header row
        this_label = int(float(parts[0]));
        this_word = parts[1];
        this_vector = np.array([float(j) for j in parts[2:]])

        if(feature_data is None):
            feature_data = np.zeros([batch_data_length, len(this_vector)], 'float');

        keys_list.append(this_word);
        y_data[len(keys_list)-1, int(this_label)] = 1; ## one hot encoding
        feature_data[len(keys_list)-1, :] = this_vector;

        if(i == 0):
            print("word 0 = ", this_word);
        

        #if(i%100 == 0):
            #print(i);
            #print(len(keys_list));
            #print(feature_data.shape);

    data_source_lines_index[this_source_type] = i;
    
    
    
    return feature_data, y_data, keys_list; 
    
    
    