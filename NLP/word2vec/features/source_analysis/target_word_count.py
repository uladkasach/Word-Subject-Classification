import numpy as np

source = 'plants_650k_export.csv';
#source = 'embeddings.csv';
#vocab_size = 30000 - 1;
target_word = 'jwh';

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
plant_vector = 0
i = 0;

with open(source) as fp:
    for line in fp:
        words = line.split(",");
        for this_word in words:
            this_word = this_word[1:-1]; # remove quotation marks at beginging and end
            #print(this_word, "-vs-", target_word);
            if(this_word == target_word):
                #print (parts[1:302]);
                plant_vector = plant_vector + 1;
                print(i);
                #print (plant_vector);
            i = i + 1;
print("All Counted."); 
print(plant_vector);
    