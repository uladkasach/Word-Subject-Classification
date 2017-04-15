import numpy as np;
import pandas as pd;
import sys;


###################################
## HP
###################################
load_limit = None;
input_mod = sys.argv[1];

####################################
## Load Dictionary
####################################
source = 'dictionary_'+input_mod+'.csv';
index = -1;
the_dictionary = [];
f = open(source, 'r');
for line in f.readlines():
    index += 1;
    word = line.strip('\n');
    the_dictionary.append(word);
    if(load_limit != None):
        if(index >= load_limit):
            break;
f.close() # not indented, this happens after the loop
#print(the_dictionary);



#######################################
## Load Assignments
#######################################
source = 'assignments_'+input_mod+'.csv';
assignments = np.loadtxt(source, dtype = 'float', delimiter = ',');
if(load_limit != None):
    assignments = assignments[0:load_limit + 1];
#print (assignments);



######################################
## Group By Assignments
######################################
df = pd.DataFrame(
    {'word': the_dictionary,
     'assignment': assignments,
    });
the_string = "";
grouped_df = df.groupby('assignment');
for key, item in grouped_df:
    this_string = (str(grouped_df.get_group(key)) + "\n\n");
    print(this_string);
    the_string += this_string;

    

######################################
## Save the data
######################################
#name_delta = sys.argv[1];
name_delta = input("Enter a name delta if you'd like save the data\n -->");
f = open('clusters/clusters_'+name_delta+'.csv', 'w+');
f.write(the_string);
f.close();