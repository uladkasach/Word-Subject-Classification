import numpy as np
import sys

#source = 'GoogleNews-vectors-negative300.txt';
#vocab_size = 3000000;

#source = 'embeddings.csv';
#vocab_size = 30000 - 1;
source = sys.argv[1];
target_word = sys.argv[3];#'plant';
n = int(sys.argv[2]); #50;
vocab_size = -1;

'''
f = open(source, 'r');
for i in range(0,10):
    first_line = f.readline()
    #print( first_line);
    word = first_line.split(" ")[0];
    print(first_line);
exit();
'''

#############
## Step 1;
## Find "plant" and record its vector
#############
plant_vector = None
i = -1;
f = open(source, 'r');
for line in f.readlines():
    i = i + 1;
    parts = line.split();
    word = parts[0];
    print (word);
    if(word == target_word):
        #print (parts[1:302]);
        plant_vector = np.array([float(i) for i in parts[1:]])
        break;
        #print (plant_vector);
    if(i == vocab_size):
        break;
if plant_vector is None:
    print("target word not found.");
    exit();
else:
    print("Target vector has been successfuly found!"); 
    
print("\n");
################
## Step 2:
## Find nearest n words to plant
################
#n = 25*2; # ------------------------------------------------------------------------------------------- HP
#vector_storage = np.zeros(shape=(n,300))
ordered_distances = [-9] * n;
#print(vector_index);
ordered_words = [""] * n;

'''
Logic:
    for every word - compute its distance from plant
    insert this distance into storage, in order of magnitude (largest to smallest)
    
    Check last index's distance (v_index[n-1, 1] to see if new distance is greater than smaller distance)
    If greater, start from bottom and "swap" down the vectors untill place is found
'''

def calculate_cosine_similarity_between(vec_a, vec_b):
    ''' 
    A dot B = |A||B|cosine(theta)
    return cosine(theta)
    '''
    
    cos = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return cos;
    
def insert_this_word_into_storage(new_word, new_vec, new_sim):
    """
    vector storage is not actually sorted, only the index is. vector takes the pushed out index position in storage (this is the lowest index if all places in storage are filled). Index is decremented untill proper place is found
    
    Note - vector storage not actually required for this task. Not implemented.
    """
    ordered_distances[n-1] = new_sim;
    ordered_words[n-1] = new_word;
    #print("here i am: ", ordered_words[n-1]);
    #print(ordered_words);
    place_found = False;
    i = 0;
    for i in range(0, n-1):
        if(place_found != False):
            break;
        this_index = n-1-i;
        next_index = n-2-i;
        this_sim = ordered_distances[this_index];
        next_sim = ordered_distances[next_index];
        #print("this_sim (" , this_sim, ") -vs- (", next_sim, ")");
        if(this_sim > next_sim):
            #print("true, bigger");
            ordered_distances[this_index] = ordered_distances[next_index];
            ordered_distances[next_index] = new_sim;
            ordered_words[this_index] = ordered_words[next_index];
            ordered_words[next_index] = new_word;
        else:
            place_found = True;
        #print(ordered_distances);
        #print(place_found, i, n-1); 
            
            
def display_current_order():
    for i in range(0,n):
        print(ordered_words[i].ljust(20), " : ", ordered_distances[i]); 
    
    
i = -1;
f = open(source, 'r');
for line in f.readlines():
    i = i + 1;
    if(i == 0): 
        continue;
        
    parts = line.split();
    this_word = parts[0];
    
    ##if(this_word == "plant"):
    ##    continue;
    
    this_vector = np.array([float(i) for i in parts[1:]])
    #print(this_vector);
    this_sim = calculate_cosine_similarity_between(this_vector, plant_vector);
    #print(this_word.ljust(10), " : ", this_sim);
    
    min_similarity = ordered_distances[n-1];
    #print(min_similarity);
    #print(this_sim);
    #print(this_sim > min_similarity);
    if(this_sim > min_similarity):
        insert_this_word_into_storage(this_word, this_vector, this_sim);
        
    if(i % 20000 == 0):
        print ("\nOrder by word ", i , ":");
        display_current_order();
        

print ("\nOrder by word ", i , ":");
display_current_order();
