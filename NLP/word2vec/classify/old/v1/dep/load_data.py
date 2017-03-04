###############
## Import Libraries
###############
import tensorflow as tf
import load_inputs as inputs
import sys
import numpy as np;
import random;
import datetime;

##########################################################################
## Return Random Batch
##########################################################################
def load_frequent_words(path, threshold):
    #######################################
    ## Load Frequent Words
    #######################################
    min_word_frequency_threshold = int(threshold);
    frequent_words = [];
    f = open(path, 'r');
    for line in f.readlines():
        parts = line.rstrip().split(",");
        #print(parts);
        word = parts[0];
        freq = int(parts[1]);
        if(freq >= min_word_frequency_threshold):
            frequent_words.append(word);
    f.close();
    return frequent_words;

def load_true_words(path):
    #######################################
    ## Load True Words
    #######################################
    true_words = [];
    f = open(path, 'r');
    for line in f.readlines():
        parts = line.rstrip().split(",");
        #print(parts);
        word = parts[0];
        true_words.append(word);
    f.close();
    #print(len(true_words));
    return true_words;

def return_random_regular_batch(data_source_path, true_labels_path, frequency_table_path, frequency_threshold, batch_size):
    global frequent_words;
    global true_words;
    global source_lines;
    global line_index;
    
    #start_batch = datetime.datetime.now()

    if 'frequent_words' not in globals():
        frequent_words = load_frequent_words(frequency_table_path, frequency_threshold);
        
    if 'true_words' not in globals():
        true_words = load_true_words(true_labels_path);
        
    if 'source_lines' not in globals():
        #print("Initializeing Source_lines");
        fp = open(data_source_path);
        source_lines = fp.readlines();
        random.shuffle(source_lines);
        fp.close();
        line_index = 0;
        
    
    one_hot_depth = inputs.one_hot_depth;
    

    
    keys_list = []; ## only supports one key per row atm
    y_data = np.zeros([batch_size, one_hot_depth], 'float');
    feature_data = None; #numpy.zeros([batch_size, len(feature_index)], 'float');
    ## Grab and parse data
    i = -1;
    
    '''
    index_limit = len(source_lines)/2;
    while i < batch_size - 1:
        line = source_lines[line_index];
        line_index += 1;
        if(line_index >= index_limit): ## Only shuffle once we get to the end of the last shuffle
            print('line index : ', line_index, ", source lines : ", len(source_lines), ". Shuffling...");
            print(source_lines[0:2]);
            random.shuffle(source_lines);
            print(source_lines[0:2]);
            line_index = 0;
            continue;
            
    '''
    
            
    random.shuffle(source_lines);
    for line in source_lines:
        if(i+2 > batch_size):
            break;
        parts = line.rstrip().split();
        this_word = parts[0];
        this_vector = np.array([float(j) for j in parts[1:]])
        #print(this_word);
        
        if(this_word not in frequent_words):
            #print("not a frequent word. skipping");
            continue;
        i += 1;


        if(this_word in true_words):
            this_label = 1;
        else:
            this_label = 0;
        #print("label = ", this_label);

        if(feature_data is None):
            feature_data = np.zeros([batch_size, len(this_vector)], 'float');

        keys_list.append(this_word);
        y_data[i, int(this_label)] = 1; ## one hot encoding
        feature_data[i, :] = this_vector;

        #if(i%100 == 0):
            #print(i);
            #print(len(keys_list));
            #print(feature_data.shape);

    ## Parse Data
    #data_keys_columns = [list_of_columns[i] for i in data_keys_index];
    #y_columns = [float(list_of_columns[i]) for i in y_index];
    #feature_columns = [float(list_of_columns[i]) for i in feature_index];
    #end_batch = datetime.datetime.now();
    #print("Shuffle Time: ", (start_shuffle - end_shuffle).total_seconds() );
    #print("Batch Time: ", (start_batch - end_batch).total_seconds() );
    return feature_data, y_data, keys_list; 
    
'''
features, labels, keys = return_random_regular_batch('../gen_features/inputs/embeddings_5.6m_basic.csv', '../../features/label_analysis/results/frequent_plant_words.txt',  '../../features/label_analysis/inputs/5.6m_basic_freq_table.csv', 10, 1000); 
for i in range(len(labels)):
    print(labels[i], " - ", keys[i]);
exit();
'''   
   

##########################################################################
## Return Regular Batch
##########################################################################
def return_regular_batch(data_source_path, batch_size):
    
    data_source_path = data_source_path[0];
    
    ## Load settings
    #y_index = inputs.label_index;
    one_hot_depth = inputs.one_hot_depth;
    #data_keys_index = inputs.keys_index;
    #record_defaults = inputs.record_defaults;
    #feature_index = list(set(list(range(len(list_of_columns)))) - set(y_index)  - set(data_keys_index));
    
    
    keys_list = []; ## only supports one key per row atm
    y_data = np.zeros([batch_size, one_hot_depth], 'float');
    feature_data = None; #numpy.zeros([batch_size, len(feature_index)], 'float');
    ## Grab and parse data
    with open(data_source_path) as fp:
        for i, line in enumerate(fp):
            if(i >= batch_size): 
                #print("batch size ("+batch_size+") reached");
                break;
            
            parts = line.rstrip().split(",");
            this_label = parts[0];
            this_word = parts[1];
            this_vector = np.array([float(j) for j in parts[2:]])
            
            if(feature_data is None):
                feature_data = np.zeros([batch_size, len(this_vector)], 'float');
            
            keys_list.append(this_word);
            y_data[i, int(this_label)] = 1; ## one hot encoding
            feature_data[i, :] = this_vector;
            
            #if(i%100 == 0):
                #print(i);
                #print(len(keys_list));
                #print(feature_data.shape);

    ## Parse Data
    #data_keys_columns = [list_of_columns[i] for i in data_keys_index];
    #y_columns = [float(list_of_columns[i]) for i in y_index];
    #feature_columns = [float(list_of_columns[i]) for i in feature_index];
    return feature_data, y_data, keys_list; 
    
    
    

##########################################################################
## Read a line of data
##########################################################################
def read_csv_data(filename_queue):
    #############################
    ## DataSource dependent inputs, 
    ############################
    #y_index = [2];
    #data_keys_index = [0, 1];
    #record_defaults = [[1], [1], [1], [0.1], [0.1], [0.1], [0.1], [0.1], [0.1]] # Default values, in case of empty columns. Also specifies the type of the decoded result.
    y_index = inputs.label_index;
    one_hot_depth = inputs.one_hot_depth;
    data_keys_index = inputs.keys_index;
    record_defaults = inputs.record_defaults;
    
    ##############################
    ## Define reader
    ##############################
    reader = tf.TextLineReader(skip_header_lines=1)
    key, next_line_string = reader.read(filename_queue)

    ##############################
    ## Define decoding
    ##############################
    list_of_columns = tf.decode_csv(next_line_string, record_defaults=record_defaults)
    
    ##############################
    ## Define feature, label, and key columns
    ##############################
    data_keys_columns = [list_of_columns[i] for i in data_keys_index];
    y_columns = [tf.to_int32(list_of_columns[i]) for i in y_index];
    feature_index = list(set(list(range(len(list_of_columns)))) - set(y_index)  - set(data_keys_index));
    feature_columns = [tf.to_float(list_of_columns[i]) for i in feature_index];

    ##############################
    ## Convert data to one hot, if not one hot already (if is already, y_index length > 1
    ##############################
    if one_hot_depth != 0:
        y_columns = tf.one_hot(y_columns[0], one_hot_depth);
        
    if one_hot_depth == 0 and len(y_index) < 2:
        print('One hot depth is not set, yet y_index is not two or more inputs (data is not one hot already). Error.');
        sys.exit();
    
    key = tf.pack(data_keys_columns);
    label = tf.pack(y_columns);
    features = tf.pack(feature_columns); 
    return features, label, key
##########################################################################


##########################################################################
## Read batches of input
##########################################################################
def batch_input_pipeline(filenames, batch_size, num_epochs=None):
    filename_queue = tf.train.string_input_producer(filenames, num_epochs=num_epochs, shuffle=True);
        
    features, label, key = read_csv_data(filename_queue)
    print(key);

    # min_after_dequeue defines how big a buffer we will randomly sample
    #   from -- bigger means better shuffling but slower start up and more
    #   memory used.
    # capacity must be larger than min_after_dequeue and the amount larger
    #   determines the maximum we will prefetch.  Recommendation:
    #   min_after_dequeue + (num_threads + a small safety margin) * batch_size
    min_after_dequeue = 100
    capacity = min_after_dequeue + 3 * batch_size
    feature_batch, label_batch, key_batch = tf.train.shuffle_batch([features, label, key], batch_size=batch_size, capacity=capacity, min_after_dequeue=min_after_dequeue)
    return feature_batch, label_batch, key_batch


