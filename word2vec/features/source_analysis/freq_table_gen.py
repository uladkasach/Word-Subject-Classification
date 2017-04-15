import sys;
import csv # to load data
import collections # to get most common words
from pathlib import Path;


######################################
## Read SysArgs
######################################
delta_mod = sys.argv[1]; 
delta_mod_save = str(sys.argv[2]);

########################################
## offer help for -h
#######################################
if(delta_mod == "-h"):
    print("example : python3 freq_table_gen.py ../embed/inputs/plants_5.6m_basic_export.csv 5.6m_basic");
    exit();
    
    
#####################################
## Generate dynamic file names
#####################################
file_path_to_read_from = delta_mod;
file_name_to_write_to = 'results/'+delta_mod_save+'_freq_table.csv';
print(file_name_to_write_to);


#######################################
## Verify that user wants to overwrite files, if files with the mod names already exist
#######################################
my_file = Path(file_name_to_write_to);
if my_file.is_file():
    print("A file name with the specified dynamic arguments you've specified (e.g., ", file_name_to_write_to, ") already exists. Are you sure you want to overwrite it?");
    result = input("YES/no: ").lower();
    print (result);
    if(result == "y" or result == "yes"):
        print("Ok! Overwriting");
        #continue
    else:
        exit();
        


#########################################
# Step 1: Load Words
#########################################
print("Loading words...");
file_name = file_path_to_read_from;
print(" -- Source filename " + file_name);
with open(file_name, 'r') as f:
  reader = csv.reader(f)
  words = list(reader)[0]
##print(words)
print(" -- Words imported to analyze: ", len(words), '\n');



#########################################
# Step 2: Count Frequencies
#########################################
frequencies = collections.Counter(words);
count = [['UNK', -1]]
count.extend(frequencies.most_common(len(frequencies.items()) - 1))
print(count[0:10]);


print("Writing to file...");
#########################################
## Step 3: Generate File
#########################################
f = open(file_name_to_write_to, 'w+')
for this_word, this_count in count:
    f.write(this_word +","+str(this_count)+'\n');  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it

print("All done!");
