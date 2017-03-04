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



#########################################################
## Read Arguments
#########################################################
if(sys.argv[1] == "-h"):
    print ("name rtrue min_freq batch_size learning_rate n_hidden_1 n_hidden_2 epochs");
    exit();

arguments = dict();
acceptable_arguments = ['random', 'min_freq', 'embedding_source', 'freq_source', 'label_source', 'name', 'split_ratio'];
for i in range(len(sys.argv)):
    if(i == 0):
        continue;
    this_argv = sys.argv[i];
    parts = this_argv.split(":");
    this_name = parts[0];
    this_value = parts[1];
    if(this_name not in acceptable_arguments):
        print(this_name, " is not an acceptable argument. Error.");
        die();
    arguments[this_name] = this_value;
    

#########################################################
## Set Default Data
#########################################################
OUTPUT_ROOT = 'results/';
sampling_choices = ['random', 'over', 'under'];
sampling = 'random';
min_freq = 10;
embedding_source = '../0_data_source/embeddings_5.6m_basic.csv';
freq_source = '../0_data_source/5.6m_basic_freq_table.csv';
label_source = '../../features/label_words/plant_words.txt';
split_ratio = '80/20';

#########################################################
## Update data to arguments
#########################################################
if('name' in arguments):
    delta_mod = arguments['name'];
else:
    print("Name is required. Error.");
    exit();
    
if('min_freq' in arguments): min_freq = arguments['min_freq'];
if('embedding_source' in arguments): embedding_source = arguments['embedding_source'];
if('freq_source' in arguments): freq_source = arguments['freq_source'];
if('label_source' in arguments): label_source = arguments['label_source'];
if('split_ratio' in arguments): label_source = arguments['split_ratio'];


    
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
    df = pd.read_csv(path, sep = ' ', header=None);
    print( df.head() );
    return df;
def label_embedding(this_word):
    global true_words;
    global frequent_words;
    if(this_word not in frequent_words):
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
embeddings_df = embeddings_df[embeddings_df['label'] != -1]; ## Remove non_frequent words. Note - this needs to happen so that words_total_size can be calculated
#print(embeddings_df.shape);
print("Shuffling embeddings...");
embeddings_df = embeddings_df.reindex(np.random.permutation(embeddings_df.index)); ## Shuffle rows in dataframe
print(embeddings_df.head());




#########################################################
## Generate Test/Train split accoring to split_ratio
#########################################################  
## Idea - sample words from distributions


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
print("Test size ", test_size, ", Train Size ", train_size);


##################
## Build data holders
##################
test_set = pd.DataFrame(columns = data_columns);
train_set = pd.DataFrame(columns = data_columns);

##################
## Initialize Drawing Indecies
##################
true_drawn = 0;
false_drawn = 0;

    
def random_sampling_draw():
    global true_ratio;
    global true_drawn;
    global false_drawn;
    global true_words;
    global false_words;
    rand = np.random.random([1]);
    #print(rand);
    #print(true_ratio);
    #########################
    ## the if draw_index > word_size switches over to the other label type when the one chosen has run out. This eliminates waiting for the distribution to choose it for us.
    #########################
    if(rand > true_ratio):
        draw = 'false';
        if(false_drawn + 1 > false_words.shape[0]):
            draw = 'true';
    else:
        draw = 'true';
        if(true_drawn + 1 > true_words.shape[0]):
            draw = 'false';
        
    if(draw == 'false'):
        row = false_words.iloc[[false_drawn]];
        false_drawn += 1;
    else:
        row = true_words.iloc[[true_drawn]];
        true_drawn += 1;
        
    if((true_drawn + false_drawn - 1) % 100 == 0):
        print(test_size,  '(', test_set.shape[0], ")","--", train_size, '(', train_set.shape[0], ")", ":", true_drawn, 'vs', false_drawn);
        
    return row;
##################
## Build testing set first, since it will be smaller
##################
while test_set.shape[0] < test_size:
    if(sampling == 'random'):
        new_row = random_sampling_draw();
    framed_row = pd.DataFrame(new_row);
    ##print(framed_row);
    test_set = pd.concat([test_set, framed_row], ignore_index=True)
##################
## Now build training set
##################
while train_set.shape[0] < train_size:
    if(sampling == 'random'):
        new_row = random_sampling_draw();
    framed_row = pd.DataFrame(new_row);
    ##print(framed_row);
    train_set = pd.concat([train_set, framed_row], ignore_index=True)    

print(test_set[['label', 0]].head());
print(train_set[['label', 0]].head());
    
    
    
#########################################################
## Shuffle Results
#########################################################
print("Shuffling Results...");
test_set = test_set.reindex(np.random.permutation(test_set.index));
train_set = train_set.reindex(np.random.permutation(train_set.index));



#########################################################
## Record Results
#########################################################
test_set.to_csv(path_or_buf=OUTPUT_ROOT+delta_mod+"_test.csv", sep=',', index = False);
train_set.to_csv(path_or_buf=OUTPUT_ROOT+delta_mod+"_train.csv", sep=',', index = False);