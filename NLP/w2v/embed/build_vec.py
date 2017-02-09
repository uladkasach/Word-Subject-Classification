##########
## Load Words
##########
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import collections
import math
import os
import random
import zipfile
import sys

import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf


import csv # to load data
import collections # to get most common words
import numpy as np
import random
import tensorflow as tf






#########################################
# Step 0: Define Hyperparameters
#########################################
print("Starting\n");
#batch_size = 4;
#num_skips = 3;
#skip_window = 12;



#########################################
# Step 1: Load Words
#########################################
print("Loading words...");

delta_mod = sys.argv[1]; #1.7m_basic
file_name = 'plants_'+delta_mod+'_export.csv';
print(" -- Source filename " + file_name);
with open('inputs/'+file_name, 'r') as f:
  reader = csv.reader(f)
  words = list(reader)[0]
##print(words)
print(" -- Words imported to analyze: ", len(words), '\n');


#########################################
# Step 2: Build the dictionary and replace rare words with UNK token.
#########################################
print("Building dictionary and replacing rarewords with UNK token...");
vocabulary_size = 60000 #50k was used for vocab size before, 1.67M for input ---------------------------------------------------------------------- HP
frequency_dependent_vocabulary = True;  #---------------------------------------------------------------------------------------------------------- HP
usable_min_frequency = 3;

if frequency_dependent_vocabulary == True:
    usable_words = 0;
    frequencies = collections.Counter(words);
    #print(type(frequencies.items()));
    for k, v in frequencies.items():
        if (v >= usable_min_frequency):
            usable_words = usable_words + 1;
    vocabulary_size = usable_words;        
else:
    vocabulary_size = vocabulary_size;
print("Vocabulary Size : ", vocabulary_size);

def build_dataset(words, vocabulary_size):
    count = [['UNK', -1]]
    count.extend(frequencies.most_common(vocabulary_size - 1))
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




#########################################
# Step 3: Function to generate a training batch for the skip-gram model.
#########################################
print("\nSetting up training batch generator...");
data_index = 0;

def generate_batch(batch_size, num_skips, skip_window):
    global data_index
    assert batch_size % num_skips == 0
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2 * skip_window + 1  # [ skip_window target skip_window ]
    buffer = collections.deque(maxlen=span)
    # print (buffer);
    # print(data_index);
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
        # print (buffer);
        # print(data_index);
    for i in range(batch_size // num_skips):
        target = skip_window  # target label at the center of the buffer
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span - 1)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[target]
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)

    #print(buffer)
    #print(data_index);
    return batch, labels

for index in range(1):
    batch, labels = generate_batch(batch_size=8, num_skips=2, skip_window=4)
    for i in range(8):
      print(batch[i], reverse_dictionary[batch[i]],
            '->', labels[i, 0], reverse_dictionary[labels[i, 0]])

    
    
######################################### 
# Step 4: Build (and train?) a skip-gram model.
#########################################
#  ---------------------------------------------------------------------- HP ---------------------------------------------------------------------- HP
batch_size = 128
embedding_size = 300  # Dimension of the embedding vector.
skip_window = 2       # How many words to consider left and right.
num_skips = 4         # How many times to reuse an input to generate a label.

# We pick a random validation set to sample nearest neighbors. Here we limit the
# validation samples to the words that have a low numeric ID, which by
# construction are also the most frequent.
valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
num_sampled = 64    # Number of negative examples to sample.

graph = tf.Graph()

with graph.as_default():
    # Input data.
    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

    # Ops and variables pinned to the CPU because of missing GPU implementation
    with tf.device('/cpu:0'):
        # Look up embeddings for inputs.
        embeddings = tf.Variable(
            tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
        embed = tf.nn.embedding_lookup(embeddings, train_inputs)

        # Construct the variables for the NCE loss
        nce_weights = tf.Variable(
            tf.truncated_normal([vocabulary_size, embedding_size],
                                stddev=1.0 / math.sqrt(embedding_size)))
        nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

    # Compute the average NCE loss for the batch.
    # tf.nce_loss automatically draws a new sample of the negative labels each
    # time we evaluate the loss.
    loss = tf.reduce_mean(
        tf.nn.nce_loss(weights=nce_weights,
                     biases=nce_biases,
                     labels=train_labels,
                     inputs=embed,
                     num_sampled=num_sampled,
                     num_classes=vocabulary_size))

    # Construct the SGD optimizer using a learning rate of 1.0.
    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

    # Compute the cosine similarity between minibatch examples and all embeddings.
    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
    normalized_embeddings = embeddings / norm
    valid_embeddings = tf.nn.embedding_lookup(
        normalized_embeddings, valid_dataset)
    similarity = tf.matmul(
        valid_embeddings, normalized_embeddings, transpose_b=True)

    # Add variable initializer.
    init = tf.initialize_all_variables()




    
    
    
    

######################################### 
# Step 5: Begin training.
#########################################
num_steps = 100000 * 6 * + 1 # ---------------------------------------------------------------------- HP

with tf.Session(graph=graph) as session:
  # We must initialize all variables before we use them.
  init.run()
  print("Initialized")

  average_loss = 0
  for step in xrange(num_steps):
    batch_inputs, batch_labels = generate_batch(
        batch_size, num_skips, skip_window)
    feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}

    # We perform one update step by evaluating the optimizer op (including it
    # in the list of returned values for session.run()
    _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
    average_loss += loss_val

    if step % 2000 == 0:
      if step > 0:
        average_loss /= 2000
      # The average loss is an estimate of the loss over the last 2000 batches.
      print("Average loss at step ", step, ": ", average_loss)
      average_loss = 0

    # Note that this is expensive (~20% slowdown if computed every 500 steps)
    if step % 10000 == 0:
      sim = similarity.eval()
      for i in xrange(valid_size):
        valid_word = reverse_dictionary[valid_examples[i]]
        top_k = 8  # number of nearest neighbors
        nearest = (-sim[i, :]).argsort()[1:top_k + 1]
        log_str = "Nearest to %s:" % valid_word
        for k in xrange(top_k):
          close_word = reverse_dictionary[nearest[k]]
          log_str = "%s %s," % (log_str, close_word)
        print(log_str)
  final_embeddings = normalized_embeddings.eval()


###############
## Save embeddings
###############
#print(type(final_embeddings));
#np.savetxt("embeddings.csv", final_embeddings, delimiter=",")
#np.savetxt("reverse_dictionary.csv", reverse_dictionary, delimiter=",")

def return_vector_at_index(index):
    vector = (reverse_dictionary[index]);
    for i in range(0, len(final_embeddings[index])):
        vector += " " + str(final_embeddings[index, i]);
    return vector;

f = open('results/embeddings_'+delta_mod+'.csv', 'w+')
for i in range(0, vocabulary_size):
    f.write(return_vector_at_index(i)+'\n');  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it


# Step 6: Visualize the embeddings.
def plot_with_labels(low_dim_embs, labels, filename='results/tsne_'+delta_mod+'.png'):
  assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
  plt.figure(figsize=(20, 20))  # in inches
  for i, label in enumerate(labels):
    x, y = low_dim_embs[i, :]
    plt.scatter(x, y)
    plt.annotate(label,
                 xy=(x, y),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
  plt.savefig(filename)

try:
  from sklearn.manifold import TSNE
  import matplotlib.pyplot as plt

  tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
  plot_only = 1000;
  low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
  labels = [reverse_dictionary[i] for i in xrange(plot_only)]
  plot_with_labels(low_dim_embs, labels)

except ImportError:
  print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")    

