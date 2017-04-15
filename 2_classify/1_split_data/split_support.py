import sys;
import numpy as np;
import random;
import pandas as pd;


def calculate_SSE_distance_between(v1, v2):
    '''
    total_E = 0;
    for i in range(len(v1)):
        this_v1_element = v1[i];
        this_v2_element = v2[i];
        this_error = (this_v1_element - this_v2_element)**2;
        total_E += this_error;
    '''
    #print(v1);
    #print(v2);
    total_E = sum(((v1 - v2))**2)
    #print(total_E);
    return total_E;

def calculate_cosine_distance_between(vec_a, vec_b):
    ''' 
    A dot B = |A||B|cosine(theta)
    return cosine(theta)
    '''
    cos = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)); ## returns cosine similarity, [0,1]
    return 1-cos;



def find_KNN(source_vector, vector_set, k, distance_type = 'SSE'):
    ## Note - we expect that source vector will be in vector set, so really we find K+1 NN and ignore the first match.
    
    ## 1) Calculate distances, into a list
    ## 2) Insert distances into pandas DF, WITH index matching vector_set to distance
    ## 3) Sort DF by distance ASC
    ## 4) Return top k excluding first vectors, min distance.
    
    #####################
    ## 1) Calc distances
    #####################
    indices = [];
    distances = [];
    for index, vector in enumerate(vector_set):
        if(distance_type == "SSE"):
            distance = calculate_SSE_distance_between(source_vector, vector);
        elif(distance_type == "cos"):
            distance = calculate_cosine_distance_between(source_vector, vector);
        else:
            print("Distance type not valid. Error.");
            exit();
        indices.append(index);
        distances.append(distance);
    
    #######################
    ## 2, 3) insert into df and sort distance ASC
    #######################
    df =  pd.DataFrame(
    {'indices': indices,
     'distances': distances,
    });
    df = df.sort(columns=['distances']);
    #print(df);
    df = df.iloc[1:1+k];
    #print(df);
    
    #######################
    ## 4) Nearest Neighbor Vectors
    #######################
    NN = [];
    for index in df['indices'].tolist():
        ##print(index);
        nearest_vector = vector_set[index];
        NN.append(nearest_vector);

    ##print(NN);
    return NN;
    
def generate_SMOTE_samples(true_set, times, distance_type = 'SSE', dev_test = False):
    times = int(times);
    #########
    ## SMOTE :
    ## The minority class is over-sampled by taking each minority class sample and introducing synthetic examples along the line segments joining any/all of the k minority class nearest neighbors. Depending upon the amount of over-sampling required, neighbors from the k nearest neighbors are randomly chosen. Our implementation currently uses five nearest neighbors. For instance, if the amount of over-sampling needed is 200%, only two neighbors from the five nearest neighbors are chosen and one sample is generated in the direction of each. Synthetic samples are generated in the following way: Take the difference between the feature vector (sample) under consideration and its nearest neighbor. Multiply this difference by a random number between 0 and 1, and add it to the feature vector under consideration.
    #########
    ## IMPLEMENTATION :
    ## (Note Fractional oversampling not yet supported)
    ## Find KNN for each row in dataset (all true vectors). K = times. For each found element in KNN, generate a synthetic sample by : (row_in_dataset - nearest_neighbor[i])*ran([0, 1]);
    
    ##########
    ## NOTE: Assuming that 1st col of DF is label, 2nd is key, 3+ is vector
    ##########
    data_columns = true_set.columns.tolist();
    additional_samples_set = [];
    vector_columns = data_columns[2:];
    if(dev_test): vector_columns = data_columns; ## test data has no labels or keys
    vector_set = true_set.as_matrix(columns = vector_columns);

    elements_added = 0;
    for index, this_vector in enumerate(vector_set):
        NN = find_KNN(this_vector, vector_set, times, distance_type = distance_type);
        #print(NN);
        
        this_vector = np.array(this_vector);
        for neighbor_vector in NN:
            gamma = random.uniform(0, 1);
            neighbor_vector = np.array(neighbor_vector);
            synth_vector = this_vector + gamma * (neighbor_vector - this_vector); ## gamma == 0 => this_vector, gamma == 1 => neighbor_vector
            ##print(synth_vector);
            row_list = [1, "synth_"+str(elements_added)];
            if(dev_test): row_list = [];
            for attr in synth_vector: row_list.append(attr);
            additional_samples_set.append(row_list);
            elements_added += 1;
            #print(row_list);
        #if(elements_added > 5): 
            #break;
    
    additional_samples_set = pd.DataFrame(additional_samples_set, columns = data_columns);
    #print(additional_samples_set);
    
    return additional_samples_set;
    