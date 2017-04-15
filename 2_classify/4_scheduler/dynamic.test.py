


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
    "dev_mode_data_limit" : [5000],
})


#############################
## Add classification arguments
############################# 

## ['name', 'source_mod', 'njobs', 'rtrue', 'dev_mode', 'kernel', 'gamma', 'degree', 'verbose', 'classifier_choice'];
classification_arguments.append({
    "classifier_choice" : ["knn"],
})
classification_arguments.append({
    "classifier_choice" : ["rf"],
    "rtrue" : [1 ],
})
classification_arguments.append({
    "classifier_choice" : ["nn"],
    "epochs" : [400],
    "learning_rate" : [0.1],
    "n_hidden_1" : [2],
    "n_hidden_2" : [2],
    "rtrue" : [50],
})

classification_arguments.append({
    "classifier_choice" : ["svm"],
    "kernel" : ["rbf"],
    "repeats_per_set" : [2],
})