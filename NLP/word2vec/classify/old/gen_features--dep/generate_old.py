##################
## Goal, each line : label, key, features
##################
import sys;
import numpy as np;
import random;

## python3 generate.py inputs/embeddings_5.4m_basic.csv ../../features/label_words/plant_words.txt one


embeddings_source = sys.argv[1];
print("\nEmbeddings sourced from", embeddings_source);

labels_source = sys.argv[2];
print("\nTrue labels sourced from", labels_source);

result_name = sys.argv[3];
print("\nTrue labels sourced from", result_name);


###############################
## Find vectors from embeddings for true keys
###############################
## Load true labels into array
true_keys = [];
f = open(labels_source, 'r');
i = 0;
for line in f.readlines():
    i += 1;
    parts = line.split();
    this_word = parts[0];
    true_keys.append(this_word)
f.close();


## run through all embeddings and if they're in true_keys, record them with true label
i = 0;
f = open(embeddings_source, 'r');
csv_strings = [];
for line in f.readlines():
    i += 1;
    parts = line.split();
    this_word = parts[0];
    
    if(this_word in true_keys):
        this_vector = np.array([float(j) for j in parts[1:]])
        csv_string = "1,"+this_word;
        for j in this_vector:
            csv_string = csv_string + "," + str(j);
        csv_strings.append(csv_string);
        
        
    if(i % 2000 == 0):
        print ("At word index", i);
        #display_current_order();
f.close();

#print(len(true_keys));
#print(len(csv_strings));
csv_strings_true_len = len(csv_strings);

################################
## Find vectors for non true keys
################################
i = 0;
f = open(embeddings_source, 'r');
for line in f.readlines():
    i += 1;
    parts = line.split();
    this_word = parts[0];
    
    if(this_word not in true_keys):
        this_vector = np.array([float(j) for j in parts[1:]])
        csv_string = "0,"+this_word;
        for j in this_vector:
            csv_string = csv_string + "," + str(j);
        csv_strings.append(csv_string);
        
        
    if(i % 2000 == 0):
        print ("At word index", i);
        #display_current_order();
    if(i+1 > csv_strings_true_len):
        break;
f.close();


#print(true_keys[0:15]);
#print(csv_strings[0:10]);


##################################
## Write normalized vectors to file
##################################
random.shuffle(csv_strings); ## shuffle true and false keys
#####
print("\nRecording Output...");
i = 0;
fw = open("results/"+result_name+".csv", 'w+');
for this_string in csv_strings:
    fw.write(this_string + "\n");
fw.close();