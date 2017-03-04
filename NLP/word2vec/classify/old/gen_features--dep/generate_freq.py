##################
## Goal, each line : label, key, features
##################
import sys;
import numpy as np;
import random;

## python3 generate_freq.py inputs/embeddings_5.6m_basic.csv ../../features/label_analysis/inputs/5.6m_basic_freq_table.csv 10 ../../features/label_analysis/results/frequent_plant_words.txt ../../features/label_analysis/results/frequent_nonplant_words.txt one 


embeddings_source = sys.argv[1];
print("Embeddings sourced from", embeddings_source);
frequencies_source = sys.argv[2];
print("Frequencies sourced from", frequencies_source);
frequencies_threshold = sys.argv[3];
print("Embeddings sourced from", embeddings_source);
true_words_source = sys.argv[4];
print("True labels sourced from", true_words_source);
false_words_source = sys.argv[5];
print("False labels sourced from", false_words_source);
result_name = sys.argv[6];
print("True labels sourced from", result_name);


#######################################
## Load Frequent Words
#######################################
file_path_to_read_frequencies_from = frequencies_source;
min_word_frequency_threshold = int(frequencies_threshold);
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


def retreive_words(filepath):
    keys = [];
    f = open(filepath, 'r');
    i = 0;
    for line in f.readlines():
        i += 1;
        parts = line.split();
        this_word = parts[0];
        if(this_word not in frequent_words):
            print(" -- warning, " + this_word + " is not a frequent word");
        keys.append(this_word)
    f.close();
    return keys;
##########################
## Load labeled words
##########################
true_keys = retreive_words(true_words_source);
false_keys = retreive_words(false_words_source);


def retreive_random_words_excluding(exclusion_keys, max_words = -1):
    i = 0;
    f = open(embeddings_source, 'r');
    keys = [];
    lines = f.readlines();
    random.shuffle(lines);
    max_words_offset = 0;
    for line in lines:
        i += 1;
        parts = line.split();
        this_word = parts[0];

        if(this_word not in exclusion_keys and this_word in frequent_words):
            keys.append(this_word);
        else:
            max_words_offset += 1;

        if(i % 2000 == 0):
            print ("At word index", i);
            #display_current_order();
            
        if(max_words - max_words_offset == i):
            break;
            
        print("\n");
        
    f.close();
    return keys 
###############################
## Load unlabled words, to be assumed as false, from embeddings
###############################
total_labeled_keys = [];
total_labeled_keys.extend(true_keys);
total_labeled_keys.extend(false_keys);
amount_of_words_to_fill = len(true_keys) * 2 - len(false_keys); ## We want double the false keys
assumed_false_keys = retreive_random_words_excluding(total_labeled_keys, amount_of_words_to_fill);
del total_labeled_keys;


def retreive_vectors_for_words(keys):
    i = 0;
    f = open(embeddings_source, 'r');
    vectors = [];
    found_keys = [];
    for line in f.readlines():
        i += 1;
        parts = line.split();
        this_word = parts[0];

        ## determine if this vector is worth grabbing
        if(this_word in keys):
            this_vector = np.array([float(j) for j in parts[1:]]);
            vectors.append(this_vector);
            found_keys.append(this_word);

        if(i % 2000 == 0):
            print ("At word index", i);
            #display_current_order();
            
            
    f.close();
    print("\n");
    return vectors, found_keys; 
##########################
## Find vectors for labeled words
##########################
true_vectors, true_keys = retreive_vectors_for_words(true_keys);
false_vectors, false_keys = retreive_vectors_for_words(false_keys);
assumed_false_vectors, assumed_false_keys = retreive_vectors_for_words(assumed_false_keys);


def convert_into_csv(label, keys, vectors):
    all_strings = [];
    for i in range(len(keys)):
        this_key = keys[i];
        this_vector = vectors[i];
        this_string = str(label) + "," + this_key; 
        for j in this_vector:
            this_string = this_string + "," + str(j);
        all_strings.append(this_string);
    return all_strings;
###########################
## Turn vectors and keys into csv lines
###########################
all_csv_lines = [];
all_csv_lines.extend(convert_into_csv(1, true_keys, true_vectors));
all_csv_lines.extend(convert_into_csv(0, false_keys, false_vectors));
all_csv_lines.extend(convert_into_csv(0, assumed_false_keys, assumed_false_vectors));
#print(all_csv_lines[0:10]);
random.shuffle(all_csv_lines); ## shuffle true and false keys


###########################
## Turn csv lines into full text
###########################
full_csv = "";
for line in all_csv_lines:
    full_csv += line + "\n";
   

##################################
## Write normalized vectors to file
##################################
print("\nRecording Output...");
fw = open("results/"+result_name+".csv", 'w+');
fw.write(full_csv);
fw.close();