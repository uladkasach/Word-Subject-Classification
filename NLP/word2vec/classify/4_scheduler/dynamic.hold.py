
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
    "SM" : [1,  3,  5,  8, 10, 15],
}
'''

'''
classification_arguments = {
    "epochs" : [400],
    "rtrue" : [7],
}


split_arguments = {
    "sampling" : ["over"],
    "SM" : [1],
}
'''

'''
python3 schedule.py set_title:RFSMOTE repeats_per_split_set:3 classifier_choice:random_forest seconds_per_chain:60 parallel:2 dev_mode:true
'''

'''
classification_arguments = {
    "njobs" : [2],
}

'''

split_arguments.append({
    "sampling" : ["SMOTE"],
    "SM" : [3,  5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["over"],
    "SM" : [3,  5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["under"],
    "SM" : [0.9, 0.7, 0.5],
})







/////////////////////////


##########################
## Initialize
###########################
split_arguments = [];
classification_arguments = [];


###########################
## Add split arguments - the splits will be generated and all will be used for each classification_argument set
############################
split_arguments.append({
    "sampling" : ["random"],
})
split_arguments.append({
    "sampling" : ["SMOTE"],
    "SM" : [3, 5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["over"],
    "SM" : [3, 5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["under"],
    "SM" : [0.9, 0.7, 0.5],
})


#############################
## Add classification arguments
############################# 

## ['name', 'source_mod', 'njobs', 'rtrue', 'dev_mode', 'kernel', 'gamma', 'degree', 'verbose', 'classifier_choice'];
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["linear"],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["poly"],
    "degree" : [2, 3, 4, 5, 6],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["rbf"],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["sigmoid"],
})

classification_arguments.append({
    "classifier_choice" : ["rf"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
})
classification_arguments.append({
    "classifier_choice" : ["nn"],
    "epochs" : [400],
    "learning_rate" : [0.1, 0.05, 0.025],
    "n_hidden_1" : [40, 30, 20, 10, 5, 2],
    "n_hidden_2" : [40, 30, 20, 10, 5, 2],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50],
})
