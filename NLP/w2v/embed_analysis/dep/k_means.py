import tensorflow as tf
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import time

def batch_feed_pipeline(i, Xi, k, indicies = None):
    '''
    Select n, randomly, such that n * d * k * bytes < 3GB
    '''
    
    bytes_per_double = 8; #8 bytes
    max_bytes = 1073741824 * 0.75; #1Gib * x ------> caps it at about 2.5gb effectivly
    used_bytes = Xi.nbytes;
    remaining_bytes = max_bytes - used_bytes;
    bytes_per_n = Xi.shape[1] * k * bytes_per_double; #dim * k * bytes
    max_n = int(np.floor(remaining_bytes/bytes_per_n));
    
    '''
    print(Xi.shape[1]);
    print(k);
    print(bytes_per_n);
    print(max_n);
    exit();
    '''
    if(i == 0):
        print("Max n per batch : ", max_n);
        #print(max_bytes);
        #print(used_bytes);
        #print(remaining_bytes);
        #print(max_n);
    
    if(Xi.shape[0] <= max_n): #if can fit all in memory, do so
        if(i == 0):
            print(" -- All data can fit in memory, batch = full sized.");
        return Xi;
    
    if(indicies == None):
        idx = np.random.choice(range(Xi.shape[0]), max_n, replace=False);    
        return_batch = Xi[idx];
    else:
        idx = indicies;
        return_batch = Xi[idx];
        assert(return_batch.shape[0] <= max_n);
    #print(return_batch.shape);
    return return_batch;
    

def KMeansClustering(Xi, k, learning_rate, max_iterations, iteration_threshold = None, status_report_rate = 100):
    ################
    ## Input
    ################
    #X = tf.placeholder_with_default(Xi, Xi.shape, name='data')
    X = tf.placeholder('float64', [None, None]);

    ################
    # Randomly select centroids from data points
    ################
    idx = np.random.choice(range(Xi.shape[0]), k, replace=False)
    Wi = Xi[idx].copy()
    W = tf.Variable(Wi, name='centroids', dtype=tf.float64)
    
    ################
    # Reshape Tensors for Calculation
    ################
    samples = X;
    centroids = W;
    expanded_vectors = tf.expand_dims(samples, 0)
    expanded_centroids = tf.expand_dims(centroids, 1)

    ################
    # Define objective of model
    ################
    raw_distances = tf.square(tf.sub(expanded_vectors, expanded_centroids));
    distances = tf.reduce_sum( raw_distances, 2)
    min_distances = tf.reduce_min(distances, 0); 
    cost = tf.reduce_sum(min_distances)  ## cost = sum of smallest distances

    '''
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost) # object which will minimize cost w.r.t. W
    '''
    
    
    

    ################
    ## Run the Model
    ################
    with tf.Session() as sess:
        
        
        sess.run(tf.global_variables_initializer());
        
        print(sess.run(W));
        sess.run(W.assign([1,2], [3,4], [5,6]));
        exit();
        
        
        
        
        last_avg_cost = 0;
        total_cost = 0;
        cost_index = 0;
        start_time = time.time();
# your code
        for i in range(max_iterations + 1):
            this_batch = batch_feed_pipeline(i, Xi, k);
            sess.run(optimizer, feed_dict={X: this_batch})
            if i % int(np.ceil(status_report_rate/20)) == 0:
                total_cost += sess.run(cost, feed_dict={X: this_batch});
                cost_index += 1;
                #print(cost_index);
                #print(int(np.ceil(status_report_rate/20)));
            if i % status_report_rate == 0:
                avg_cost = total_cost/cost_index;
                elapsed_time = time.time() - start_time;
                #Wtest = sess.run(Wc[0,:,:]);
                #print("w:", Wtest);
                print('Iteration {}, avg cost {}, delta_t {}'.format(i, avg_cost, elapsed_time))
                if(np.absolute(last_avg_cost - avg_cost) < iteration_threshold):
                    print('iteration threshold broken');
                    break;
                last_avg_cost = avg_cost;
                total_cost = 0;
                cost_index = 0;
                start_time = time.time();

        W_learned = sess.run(W)
        #dists = sess.run(distances);
        y = sess.run(tf.arg_min(distances, 0), feed_dict={X: this_batch}); #assignments, return the index of the lowest distance for each 'n'/row/'element'

        centroids = W_learned;
        assignments = y;

    return centroids, assignments


########################################
## Hyper Parameters
########################################
k = 3; # Number of clusters
learning_rate = 0.001; #learning rate for gradient descent
max_iterations = 1000;
iteration_threshold = 0.05; 
reporting_rate = 10;


if(False):
    ########################################
    ## Load Data
    ########################################
    #source = 'GoogleNews-vectors-negative300.txt';
    #vocab_size = 3000000;
    source = 'embeddings.csv';
    vocab_size = 30000 - 1;
    vocab_size = 1200;

    the_vectors = np.zeros(shape=(vocab_size,300));
    the_dictionary = [""] * vocab_size;
    f = open(source, 'r');
    for i in range(0, vocab_size):
        first_line = f.readline()
        parts = first_line.split(" ");
        word = parts[0];
        vector = np.array(parts[1:302], dtype=float);
        #print (plant_vector);
        the_dictionary[i] = word;
        the_vectors[i, :] = vector;


    #print(dists);
    #print(assignemnts[0:10]);
    centroids, assignments = KMeansClustering(the_vectors, k, learning_rate, max_iterations, iteration_threshold, reporting_rate); 

    print(assignments[0:50]);

    '''
    f = open('k_means_results/centroids.csv', 'w+');
    for i in range(0, vocabulary_size):
        f.write(return_vector_at_index(i)+'\n');  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    '''

    f = open('k_means_results/dictionary.csv', 'w+');
    for word in the_dictionary:
        f.write(word+'\n');
    f.close();
    #np.savetxt("k_means_results/dictionary.csv", the_dictionary, delimiter=",");
    np.savetxt("k_means_results/centroids.csv", centroids, delimiter=",");
    np.savetxt("k_means_results/assignments.csv", assignments, delimiter=",");



#######
## Test Data
#######
if(True):
    Xi, yi = datasets.make_blobs(500, random_state=1111)
    print(yi[0:10]);
    Xi = Xi.astype(np.float32)
    data = Xi;

    centroids, assignments = KMeansClustering(data, k, learning_rate, max_iterations, iteration_threshold, reporting_rate); 


    ##############
    ## ploting test data
    ##############
    plt.scatter(*Xi.T, c='k', lw=0);
    plt.scatter(*Xi.T, c=assignments, lw=0, vmax=k + 0.5, label='data');
    plt.scatter(*centroids.T, c='none', s=100, edgecolor='r', lw=2, label='prototypes');
    plt.legend(scatterpoints=3);
    plt.show()