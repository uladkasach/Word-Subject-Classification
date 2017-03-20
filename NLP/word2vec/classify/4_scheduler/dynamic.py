
# = "nn";

seconds_per_chain = 3*60; #3 if nn

'''
classification_arguments = { ## NN
    "epochs" : [400],
    "learning_rate" : [0.1, 0.05, 0.025, 0.01],
    "n_hidden_1" : [30, 20, 10, 5],
    "n_hidden_2" : [30, 20, 10, 5, 2],
    "rtrue" : [7, 10, 20, 30, 40, 50, 60, 70],
}

classification_arguments = {
    "a" : [1,2,3],
    "b" : [1,2,3],
    "c" : [1,2,3],
    }

split_arguments = {
    "a" : [1, 2],
    "b" : [3],
}
'''

'''
classification_arguments = {
    "source_mod" : ["OSM1-samplingover", "OSM3-samplingover", "OSM5-samplingover", "OSM8-samplingover", "OSM10-samplingover", "OSM15-samplingover"],
    "epochs" : [400],
    "learning_rate" : [0.1, 0.05, 0.025],
    "n_hidden_1" : [40, 30, 20, 10, 5, 2],
    "n_hidden_2" : [40, 30, 20, 10, 5, 2],
    "rtrue" : [1, 2, 3, 4],
}
'''

'''
split_arguments = {
    "sampling" : ["over"],
    "OSM" : [1,  3,  5,  8, 10, 15],
}
'''

'''
classification_arguments = {
    "epochs" : [400],
    "rtrue" : [7],
}


split_arguments = {
    "sampling" : ["over"],
    "OSM" : [1],
}
'''



split_arguments = {
    "sampling" : ["over"],
    "OSM" : [1, 2, 3,  5,  8, 10, 15],
}
classification_arguments = {
    "njobs" : [2],
}
