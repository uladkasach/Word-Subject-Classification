#####################
## Goal : Split data into test and train datasets
## Constraits :
##      - User can pick minimum frequency for W2V words to be included (tunable insight)
##      - User can pick whether to oversample, undersample, or randomsample words
##      - User can choose whether to synthetically oversample 
##          - Basic SMOTE
##          - Normal Dist SMOTE
#######################



import sys;
import numpy as np;
import random;
import pandas as pd;
import split_support;


#########################################################
## Read Arguments
#########################################################
if(sys.argv[1] == "-h"):
    print ("python3 split_data.py name:test_split split_ratio:70/30 sampling:random dev_mode_data_limit:3000");
    exit();

arguments = dict();
acceptable_arguments = ['min_freq', 'embedding_source', 'freq_source', 'label_source', 'name', 'split_ratio', 'sampling', 'sampling_multiplier', 'SM', 'dev_mode_data_limit', 'dist'];
for i in range(len(sys.argv)):
    if(i == 0):
        continue;
    this_argv = sys.argv[i];
    parts = this_argv.split(":");
    this_name = parts[0];
    this_value = parts[1];
    if(this_name not in acceptable_arguments):
        print(this_name, " is not an acceptable argument. Error.");
        exit();
    arguments[this_name] = this_value;
    

#########################################################
## Set Default Data
#########################################################
OUTPUT_ROOT = 'results/';
sampling_choices = ['random', 'over', 'under', 'SMOTE', 'SMOTE_NORM'];
sampling = 'random';
min_freq = 10;
split_ratio = '70/30';
DEV_MODE_DATA_LIMIT = None;
distance_measure = 'SSE'; # used for SMOTE 
##
#embedding_source = '../0_data_source/embeddings_5.6m_basic.csv';
#freq_source = '../0_data_source/5.6m_basic_freq_table.csv';
#label_source = '../../features/label_words/plant_words.txt';
#skiprows = 0;
embedding_source = '../0_data_source/GoogleNews-vectors-negative300.csv';
freq_source = None;
label_source = '../../features/label_words/google_plant_words.txt';
skiprows = 1;


#########################################################
## Update data to arguments
#########################################################
if('name' in arguments):
    delta_mod = arguments['name'];
else:
    print("Name is required. Error.");
    exit();
    
if('min_freq' in arguments): min_freq = int(arguments['min_freq']);
if('embedding_source' in arguments): embedding_source = arguments['embedding_source'];
if('freq_source' in arguments): freq_source = arguments['freq_source'];
if('label_source' in arguments): label_source = arguments['label_source'];
if('split_ratio' in arguments): split_ratio = arguments['split_ratio'];
if('dev_mode_data_limit' in arguments): DEV_MODE_DATA_LIMIT = int(arguments['dev_mode_data_limit']);
if('dist' in arguments): 
    distance_measure = arguments['dist'];
    if(distance_measure not in ['SSE', 'cos']):
        print(distance_measure, " is not a valid distance measure for SMOTE. Error.");
        exit();
if('sampling' in arguments): 
    desired_sampling = arguments['sampling'];
    if(desired_sampling not in sampling_choices):
        print(desired_sampling, " is not a valid sampling choice. Error");
        exit();
    sampling = desired_sampling;

if(sampling == 'over' or sampling == "under" or sampling == "SMOTE"):
    if('sampling_multiplier' not in arguments and 'SM' not in arguments ):
        print("sampling_multiplier / SM must be defined when using over sampling. Error");
        exit();
    if('SM' in arguments):
        sampling_multiplier = float(arguments['SM']);
    else:
        sampling_multiplier = float(arguments['sampling_multiplier']);
        
if(sampling == "over"):
    if(sampling_multiplier < 1):
        print("sampling_multiplier msut be greater than one for over sampling, otherwise you're not sampling. Error.");
        exit();
if(sampling == "under"):
    if(sampling_multiplier > 1):
        print("sampling_multiplier must be less than than one for under sampling, otherwise you're not sampling correctly. Error.");
        exit();
if(sampling == "SMOTE"):
    if(sampling_multiplier < 1):
        print("sampling_multiplier msut be greater than one for SMOTE sampling, otherwise you're not sampling. Error.");
        exit();
    
    
#########################################################
## Load Data
#########################################################   
def retreive_words(filepath):
    keys = [];
    f = open(filepath, 'r');
    i = 0;
    for line in f.readlines():
        i += 1;
        parts = line.split();
        this_word = parts[0];
        keys.append(this_word)
    f.close();
    return keys;
def retreive_frequent_words(frequency_table_path, frequency_threshold):
    if(freq_source is None):
        print("Frequent words not found. Not Frequency into acount.");
        return None; 
    min_word_frequency_threshold = int(frequency_threshold);
    frequent_words = [];
    f = open(frequency_table_path, 'r');
    for line in f.readlines():
        parts = line.rstrip().split(",");
        #print(parts);
        word = parts[0];
        freq = int(parts[1]);
        if(freq >= min_word_frequency_threshold):
            frequent_words.append(word);
    f.close();
    print(" -- Words frequent enough in total: ", len(frequent_words), '\n');
    return frequent_words;
def retrieve_embeddings(path):
    df = pd.read_csv(path, sep = ' ', header=None, skiprows = skiprows, nrows = DEV_MODE_DATA_LIMIT);
    #print( df.head() );
    return df;
def label_embedding(this_word):
    global true_words;
    global frequent_words;
    if(frequent_words is not None and this_word not in frequent_words):
        return -1;
    elif(this_word in true_words):
        return 1;
    else:
        return 0;
#########################################################  
print("Loading data...");
true_words = retreive_words(label_source);
frequent_words = retreive_frequent_words(freq_source, min_freq);
embeddings_df = retrieve_embeddings(embedding_source);
print("Labling and cleaning embeddings...");
embeddings_df['label'] = embeddings_df.apply(lambda row: label_embedding(row[0]), axis=1); ## label rows
cols = embeddings_df.columns.tolist();
embeddings_df = embeddings_df[cols[-1:] + cols[:-1]]; ## Move label to first column
#print(embeddings_df.shape);
embeddings_df = embeddings_df[embeddings_df['label'] != -1]; ## Remove non_frequent words. Note - this needs to happen so that words_total_size can be calculated; frequent_words
#print(embeddings_df.shape);
print("Shuffling embeddings...");
embeddings_df = embeddings_df.reindex(np.random.permutation(embeddings_df.index)); ## Shuffle rows in dataframe
#print(embeddings_df.head());




#########################################################
## Generate Test/Train split accoring to split_ratio
#########################################################  


##################
## Seperate Words
##################
true_words = embeddings_df[embeddings_df['label'] == 1];
false_words = embeddings_df[embeddings_df['label'] == 0];
data_columns = embeddings_df.columns.tolist();
del embeddings_df;


##################
## Generate Statistics
##################
parts = split_ratio.split('/');
total_words_size = true_words.shape[0] + false_words.shape[0];
true_words_size = true_words.shape[0];
true_ratio = true_words_size / total_words_size; 
test_size = int(np.ceil(int(parts[1])/100 * total_words_size));
train_size = (total_words_size) - test_size;

#######
## if upsampling or downsampling training data, reflect that before displaying training size.
#######
print("True Words Size ", true_words_size, ", Total Words Size ", total_words_size, ", True Ratio = ", true_ratio);
print("Test size ", test_size, ", Train Size ", train_size);


##################
## Calculate True, False Elements for Test Set
##################
test_true_size = int(np.ceil(test_size * true_ratio));
test_false_size = int(test_size - test_true_size);

##################
## Derive True and False sets for Test and Train splits
##################
print("Splitting train and test data...");
test_true_set = true_words[0:test_true_size];
test_false_set = false_words[0:test_false_size];
train_true_set = true_words[test_true_size+1:];
train_false_set = false_words[test_false_size+1:];

##################
## Modify Training's True and False sets as dictated by sampling
##################
if(sampling == 'over'):
    #sampling_multiplier
    train_true_size = train_true_set.shape[0];
    additional_true_samples_required = int(np.ceil((sampling_multiplier - 1) * train_true_size));
    orig_additional_true_samples_required = additional_true_samples_required;
    additional_samples_set = pd.DataFrame(columns = data_columns);
    while (additional_true_samples_required > train_true_size):
        #print('additional required more than trainset (', train_true_size, ")");
        additional_true_samples_required -= train_true_size;
        #print('now additional required = ', additional_true_samples_required);
        additional_samples_set = pd.concat([additional_samples_set, train_true_set], ignore_index=True);
    repeated_samples = train_true_set.sample(n=additional_true_samples_required);
    additional_samples_set = pd.concat([additional_samples_set, repeated_samples], ignore_index=True);
    
    train_true_set = pd.concat([train_true_set, additional_samples_set], ignore_index=True);
    print('With oversampling, train_true_set is now at length', train_true_set.shape[0], ' - originally ', train_true_size);
if(sampling == 'under'):
    #sampling_multiplier
    train_false_size = train_false_set.shape[0];
    total_false_samples_required = int(np.floor(sampling_multiplier * train_false_size));
    train_false_set = train_false_set.sample(n=total_false_samples_required);
    print('With undersampling, train_false_set is now at length', train_false_set.shape[0], ' - originally ', train_false_size);
if(sampling == 'SMOTE'):
    #sampling_multiplier
    train_true_size = train_true_set.shape[0];
    additional_true_samples_required = int(np.ceil((sampling_multiplier - 1) * train_true_size));
    times = sampling_multiplier - 1;
    additional_samples_set = split_support.generate_SMOTE_samples(train_true_set, times, distance_type = distance_measure);		
    #additional_samples_set = pd.concat([additional_samples_set, repeated_samples], ignore_index=True);
    train_true_set = pd.concat([train_true_set, additional_samples_set], ignore_index=True);
    print('With oversampling, train_true_set is now at length', train_true_set.shape[0], ' - originally ', train_true_size);


##################
## Combine True and False Sets
##################
print("Combining true and false sets...");
test_set = pd.concat([test_true_set,test_false_set], ignore_index=True);
train_set = pd.concat([train_true_set, train_false_set], ignore_index=True);

    
#########################################################
## Shuffle Results
#########################################################
print("Shuffling Results...");
test_set = test_set.reindex(np.random.permutation(test_set.index));
train_set = train_set.reindex(np.random.permutation(train_set.index));


print('Test set head...');
print(test_set[['label', 0]].head());
print('Train set head...');
print(train_set[['label', 0]].head());

#########################################################
## Record Results
#########################################################
test_set.to_csv(path_or_buf=OUTPUT_ROOT+delta_mod+"_test.csv", sep=' ', index = False);
train_set.to_csv(path_or_buf=OUTPUT_ROOT+delta_mod+"_train.csv", sep=' ', index = False);