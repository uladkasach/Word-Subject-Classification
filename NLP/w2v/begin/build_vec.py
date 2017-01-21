##########
## Load Words
##########
import csv # to load data
import collections # to get most common words
print("Starting\n");


#########################################
# Step 1: Load Words
#########################################
print("Loading words...");
with open('plants_(-)50k_export.csv', 'r') as f:
  reader = csv.reader(f)
  words = list(reader)[0]
##print(words)
print ("Words imported to analyze: ", len(words), '\n');



#########################################
# Step 2: Build the dictionary and replace rare words with UNK token.
#########################################
print("Building dictionary and replacing rarewords with UNK token...");
vocabulary_size = 5000 #50k was used for vocab size before, 167k for input

def build_dataset(words, vocabulary_size):
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary) # assign each word in vocabulary an ID based on position in frequency 
  data = list()
  unk_count = 0
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    else:
      index = 0  # dictionary['UNK']
      unk_count += 1
    data.append(index)
  count[0][1] = unk_count
  reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
  return data, count, dictionary, reverse_dictionary

data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
#del words  # Hint to reduce memory.
print('15 most common words (inc. UNK)\n ', count[:15])
print('Sample data :\n ', data[:10], '\n ', words[:10])




