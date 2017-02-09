import sys;
import numpy as np;

source = sys.argv[1];
print("\nWorking with file", source);


###############################
## Get sum to calculate mean
###############################
print("\nSumming and calculating mean...");
the_sum = None;
f = open(source, 'r');
i = -1;
for line in f.readlines():
    i += 1;
    parts = line.split();
    this_vector = np.array([float(i) for i in parts[1:]])

    if(the_sum is None):
        the_sum = np.zeros(this_vector.shape);
        print(the_sum.shape);
    
    the_sum += this_vector;
    
    if(i % 2000 == 0):
        print ("At word index", i);
        #display_current_order();
f.close();
the_mean = the_sum / i;

#print (the_mean);

##################################
## Write normalized vectors to file
##################################
print("\nRecording Normalized Inputs...");
i = 0;
f = open(source, 'r');
fw = open(source[0:-4] + "_norm.csv", 'w+');
for line in f.readlines():
    i += 1;
    parts = line.split();
    this_word = parts[0];
    this_vector = np.array([float(i) for i in parts[1:]])

    normalized_vector = this_vector / the_mean;
    this_string = this_word;
    for this_value in normalized_vector:
        this_string += " " + str(this_value);
    fw.write(this_string + "\n");
    
    if(i % 2000 == 0):
        print ("At word index", i);
        #display_current_order();
f.close();
fw.close();