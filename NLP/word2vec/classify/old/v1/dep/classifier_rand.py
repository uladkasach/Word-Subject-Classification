###########################################################
## Logistic Regression with Stochastic Gradient Descent Training
############################################################
import tensorflow as tf
import numpy as np
import pandas as pd
import sys
import os
import time


################
## Import Inputs
################
import load_data
import save_data
import results_analysis.analysis as results_analysis


if(sys.argv[1] == "-h"):
    print ("name rtrue min_freq batch_size learning_rate n_hidden_1 n_hidden_2 epochs");
    exit();

for i in range(len(sys.argv)):
    if(i == 0):
        continue;
    this_argv = sys.argv[i];
    
    parts = this_argv.split(":");
    if(parts[0] == "name" or parts[0] == "n"):
        delta_mod = parts[1];
    elif(parts[0] == "rtrue"):
        R_True = float(parts[1]);
    elif(parts[0] == "min_freq"):
        FREQUENCIES_THRESHOLD = int(parts[1]);
    elif(parts[0] == "batch_size"):
        batch_size = int(parts[1]);
    elif(parts[0] == "learning_rate"):
        learning_rate = float(parts[1]);
    elif(parts[0] == 'n_hidden_1'):
        n_hidden_1 = int(parts[1]);
    elif(parts[0] == 'n_hidden_2'):
        n_hidden_2 = int(parts[1]);
    elif(parts[0] == 'epochs'):
        EPOCHS = int(parts[1]);
    
if( 'delta_mod' not in locals()):
    print ("Name must be defined with name:<name> / n:<name>");
    exit();
    


###########################################################################
## Define Variables
###########################################################################

###################################
## Hyper Parameters
###################################
if 'EPOCHS' not in locals():
    EPOCHS = 100;
if 'FREQUENCIES_THRESHOLD' not in locals():
    FREQUENCIES_THRESHOLD = 10;
if 'R_True' not in locals():
    R_True = 77;
R_False = 1;
if 'batch_size' not in locals():
    batch_size = 2000;
if 'learning_rate' not in locals():
    learning_rate = 0.05;
if 'n_hidden_1' not in locals():
    n_hidden_1 = 10 # 1st layer number of features
if 'n_hidden_2' not in locals():
    n_hidden_2 = 4 # 2nd layer number of features

'''
#########
### Exponentially decreasing learning rate
#########
starter_learning_rate = 0.05; #https://www.tensorflow.org/versions/r0.9/api_docs/python/train.html#exponential_decay
global_step = tf.Variable(0, trainable=False)
#learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step, 200, 0.96, staircase=True)
#learning_rate = tf.Print(learning_rate, [learning_rate], "LR");
'''

###################################
## Data Source Variables / Ops
###################################
if(False):
    feature_batch, label_batch, key_batch = load_data.return_regular_batch([INPUT_SOURCE], batch_size);
    feature_count = feature_batch.shape[1];
    label_count = label_batch.shape[1];
else:
    feature_batch, label_batch, key_batch = load_data.return_random_regular_batch(EMBEDDINGS_SOURCE, TRUE_LABELS_SOURCE,  FREQUENCIES_SOURCE, FREQUENCIES_THRESHOLD, batch_size); 
    feature_count = feature_batch.shape[1];
    label_count = label_batch.shape[1];
    
    

###################################
# Network Parameters
###################################
n_input = feature_count 
n_classes = label_count 
    

    
###################################
# tf Graph input
###################################
x = tf.placeholder(tf.float32, [None, feature_count]) ## Features
y = tf.placeholder(tf.float32, [None, label_count]) ## True Values


###################################
# Create model
###################################
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer    
    

###################################
# Store layers weight & bias
###################################
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

###################################
# Construct model
###################################
pred = multilayer_perceptron(x, weights, biases)
perc_pred = tf.nn.softmax(pred);

#########
# Define loss and optimizer
##########
#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y)) ## Calculates cross entropy, taking into account edge softmax cases (predicitons of 0);
#cost = tf.reduce_mean(tf.nn.weighted_cross_entropy_with_logits(pred, y, POS_WEIGHT)); ## Used to handle unbalanced classes better

class_weights =  tf.constant([R_False, R_True], shape=[2, 1], dtype='float'); #42k total data points, 38k neg, 480 pos
weight_per_label = tf.matmul(y, class_weights);
preweight_cost = tf.nn.softmax_cross_entropy_with_logits(pred, y);
cost_vector = (tf.mul(tf.transpose(weight_per_label), preweight_cost));
cost = tf.reduce_mean(cost_vector);


train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)



###############################
## Initialize variables/ops
###############################
init = tf.global_variables_initializer() ## initialization operation


################################
## Evaluate Model
################################
max_pred = tf.argmax(pred,1);
correct_prediction = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


with tf.Session() as sess:
    sess.run(init);
    
    # Start populating the filename queue.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    #for i in range(1200):
        # Retrieve a single instance:
    #print(col1);
    #print(sess.run([results]))
    #print(example);
    
    
    epochs = EPOCHS;
    display_ratio = 200;
    
    ## for tracking cost,acc per epoch
    training_progress = pd.DataFrame(columns =  ["epoch", "cost", "accuracy"]);
    
    for i in range(epochs):
        #batch_feature, batch_label, batch_key = sess.run([feature_batch, label_batch, key_batch]);
        #batch_feature, batch_label, batch_key = load_data.return_regular_batch([INPUT_SOURCE], batch_size);
        batch_feature, batch_label, batch_key = load_data.return_random_regular_batch(EMBEDDINGS_SOURCE, TRUE_LABELS_SOURCE,  FREQUENCIES_SOURCE, FREQUENCIES_THRESHOLD, batch_size); 
        
        if(i == 0):
            start_time = time.time()
            print ('Init Cost : ', end = '');
            print (sess.run(cost, feed_dict={x: batch_feature, y : batch_label}));
        
        if(i % (epochs/display_ratio) == 0 and i != 0):
            end_time = time.time();
            print ('Epoch %6d' % i, end = '');
            print(' ... cost : ', end = '');
            this_cost = (sess.run(cost, feed_dict={x: batch_feature, y : batch_label}));
            print ('%10f' % this_cost, end = '');
            print (',  acc : ', end = '');
            this_acc = (sess.run(accuracy, feed_dict={x: batch_feature, y : batch_label}))
            print ('%10f' % this_acc, end = '');
            #print(' - lr : ', end = ''); 
            #print ('%10f' % sess.run(learning_rate), end = '');
            print (',  dt : ', end = '');
            delta_t = end_time - start_time;
            print ('%10f' % delta_t, end = '');
            print('');
            
            #print("Pred -vs- Label:");
            #print(sess.run(pred[0:10],  feed_dict={x: batch_feature, y : batch_label}));
            #print(batch_label[0:10]);
            
            training_progress.loc[i] = [i, this_cost, this_acc];
            start_time = time.time()

        sess.run(train_step, feed_dict={x: batch_feature, y : batch_label})
    
    print ('Final Cost : ', end = '');
    print (sess.run(cost, feed_dict={x: batch_feature, y : batch_label}));
    print ('Final Learning Rate : ', end = '');
    #print (sess.run(learning_rate));
    
    sumacc = 0;
    for i in range(10):
        #batch_feature, batch_label, batch_key = sess.run([feature_batch, label_batch, key_batch]);
        batch_feature, batch_label, batch_key = load_data.return_random_regular_batch(EMBEDDINGS_SOURCE, TRUE_LABELS_SOURCE,  FREQUENCIES_SOURCE, FREQUENCIES_THRESHOLD, batch_size); 
        predictions = (sess.run(perc_pred, feed_dict={x: batch_feature, y : batch_label}))
        max_predictions = (sess.run(max_pred, feed_dict={x: batch_feature, y : batch_label}))
        acc = (sess.run(accuracy, feed_dict={x: batch_feature, y : batch_label}))
        ## print(acc);
        sumacc += acc;
    sumacc = sumacc/10;
    print ('Average Acc : ', end = '');
    print (sumacc);
    
    coord.request_stop()
    coord.join(threads)
    
    
    
    ########
    ## create results dataframe
    ########
    #values = [batch_key, batch_label[:, 0], batch_label[:, 1], predictions[:, 0], predictions[:, 1]];
    results_dataframe = pd.DataFrame();
    results_dataframe["same"] = np.array(np.array((batch_label[:, 1]), 'int') == max_predictions, 'int');
    results_dataframe["is_plant"] = np.array((batch_label[:, 1]), 'int');
    results_dataframe["pred_plant"] = max_predictions;
    results_dataframe["key"] = batch_key;
    results_dataframe["pred_0"] = predictions[:, 0];
    results_dataframe["pred_1"] = predictions[:, 1];
    
    
    ################################
    ## Offer to save training results
    ################################
    #print(training_progress);
    save_data.offer(training_progress, results_dataframe, delta_mod = delta_mod)

    
    #################################
    ## Offer to classify all/-vs-/rest of embeddings
    #################################
    #print('Type `yes` to classify rest of the embeddings.') 
    #result = sys.stdin.readline().rstrip();
    result = 't';
    if (result == 'yes' or result == 'y' or True):

        #######################################
        ## Load Frequent Words
        #######################################
        file_path_to_read_frequencies_from = FREQUENCIES_SOURCE;
        min_word_frequency_threshold = int(FREQUENCIES_THRESHOLD);
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
        
        
        ####################
        ## Load All Data into Memory
        ####################
        i = 0;
        f = open(EMBEDDINGS_SOURCE, 'r');
        all_keys = [];
        all_vectors = [];
        for line in f.readlines():
            i += 1;
            parts = line.split();
            this_word = parts[0];
            
            
            if(i % 2000 == 0):
                print ("At word index", i);
                #display_current_order();
            
            if(this_word not in frequent_words):
                continue;
                
            all_keys.append(this_word);
            this_vector = np.array([float(j) for j in parts[1:]]);
            all_vectors.append(this_vector);

        f.close();

        all_vectors = np.array(all_vectors, 'float');
        print(len(all_keys));
        print(all_vectors.shape);
        
        
        predictions = (sess.run(perc_pred, feed_dict={x: all_vectors}))
        max_predictions = (sess.run(max_pred, feed_dict={x: all_vectors}))
        
        classification_df = pd.DataFrame();
        classification_df["pred_plant"] = max_predictions;
        classification_df["key"] = all_keys;
        classification_df["pred_0"] = predictions[:, 0];
        classification_df["pred_1"] = predictions[:, 1];
        
        print(classification_df);
        
        save_data.offer(classification_df, classification_df, 'two', delta_mod = delta_mod)
    
    #################################
    ## Save Hyperparameter config
    #################################
    epochs = EPOCHS;
    rtrue = R_True;
    min_freq = FREQUENCIES_THRESHOLD;
    hyperstring = "";
    hyperparamlist = ['delta_mod',  'epochs',  'batch_size', 'learning_rate', 'n_hidden_1', 'n_hidden_2', 'min_freq', 'rtrue'];
    for name in hyperparamlist:
        name_of_var = name;
        val_of_var = eval(name);
        hyperstring += name_of_var + " : " + str(val_of_var) + "\n";

    myfile = open("results/"+delta_mod+"_z_hyperparams.txt", "w+");
    myfile.write(hyperstring);
    myfile.close();
    print("Hyperparameters written.");
    
    
    print("Staring results analysis...");
    results_analysis.main(delta_mod);
    

del sess;
sys.exit();    

